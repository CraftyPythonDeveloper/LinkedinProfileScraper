import requests
import scrapy
from scrapy.exceptions import CloseSpider
import random
from urllib.parse import quote
import re
import json
from datetime import datetime
from scrapy.utils.project import get_project_settings


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    # allowed_domains = ["www.cse.google.com"]
    settings = get_project_settings()

    def normalise_text(self, text):
        return re.sub(r"[^A-Za-z0-9 .,]", " ", text)

    def __init__(self, search, **kwargs):
        super().__init__(search, **kwargs)
        self.heroku_url_split_at = self.settings["PROXY_SETTINGS"].get("PROXY_ROUTE", "get?url=")
        self.search_query = list(map(str.strip, search.split(",")))
        # self.page = 0
        self.pages_to_scrape = self.settings.get("MAX_PAGE_CRAWL")
        if self.pages_to_scrape is None:
            self.pages_to_scrape = 10
        self.user_agent = random.choice(self.settings.get("USER_AGENT"))
        if self.user_agent is None:
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                              'Chrome/98.0.4758.102 Safari/537.36'
        self.cse_api = self.settings.get("CSE_API_URL")
        if self.cse_api is None:
            self.cse_api = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com" \
                           "&cselibv=921554e23151c152&cx=011658049436509675749:gkuaxghjf5u&q={query}&safe=off&cse_tok={" \
                           "cse_token}&sort=&exp=csqr,cc&callback=google.search.cse.api{random_number}&start={" \
                           "page_number} "

        self.header = {
            'authority': 'cse.google.com',
            'user-agent': self.user_agent,
            'accept': '*/*',
            'sec-gpc': '1',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://recruitmentgeek.com/',
            'accept-language': 'en-US,en;q=0.9'
        }

    def start_requests(self):
        urls = [
            # self.cse_api+str(self.page*10)
            {q: self.cse_api.format(query=quote(q), cse_token=self.cse_token(),
                                    random_number=random.randint(0, 20000), page_number=0)}
            for q in self.search_query
        ]
        for url in urls:
            query = list(url.keys())[0]
            self.logger.debug(f"Start url is {url.get(query)}")
            yield scrapy.Request(url=url.get(query), callback=self.parse, headers=self.header,
                                 meta={"search_query": query, "current_page": 0, "current_url": url.get(query)})

    def parse(self, response):
        # self.logger.warning(f"request -- {response.request.headers}")
        query = response.meta.get("search_query")
        pg_no = response.meta.get("current_page")
        current_url = response.meta.get("current_url")
        if pg_no is None:
            pg_no = response.meta.get("nxt_pg")
        if response.status != 200:
            raise CloseSpider(f"received {response.status}")
        json_response = json.loads(response.text.split("(", maxsplit=1)[1].rsplit(")", maxsplit=1)[0])
        json_response = json_response.get("results")
        # with open(f"{pg_no}.json", "w") as f:
        #     json.dump(json_response, f)
        if json_response is None:
            self.logger.error("No More results or caught by google")
            return
        for i in json_response:
            try:
                now = datetime.now()
                name, org, degs = self.title_extractor(i)
                yield {"Date": now.strftime("%d-%m-%Y"), "Time": now.strftime("%H:%M:%S"),
                       "Name": self.normalise_text(name), "Designation": self.normalise_text(degs),
                       "Organisation": self.normalise_text(org),
                       "Description": self.normalise_text(i["contentNoFormatting"].replace("\n", " ")),
                       "ProfileUrl": i["url"],
                       "Query": query, "Page": pg_no // 10}
            except Exception as e:
                self.logger.error("exception raise while parsing api response -- %s", e)
                # print(i)
                continue

        url_split = current_url.split("start=")
        next_pg_no = int(url_split[1]) + 10
        base_url = url_split[0]
        if "heroku" in base_url:
            # heroku url example https://dry-wave-29207.herokuapp.com/get?url=
            heroku_split = base_url.split(self.heroku_url_split_at)
            base_url = heroku_split[1]
        next_page = f"{base_url}start={next_pg_no}"
        if next_pg_no >= (self.pages_to_scrape * 10):
            self.logger.debug(f"scrapped {self.pages_to_scrape} pages, closing spider..")
            return
        else:
            self.logger.debug(f"next page number {next_pg_no}")
            self.logger.debug(f"new url {next_page}")
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.header,
                                 meta={"search_query": query, "nxt_pg": next_pg_no, "current_url": next_page})

    def cse_token(self):
        url = self.settings.get("CSE_TOKEN_URL")
        if url is None:
            url = "https://cse.google.com/cse.js?cx=011658049436509675749:gkuaxghjf5u"
        raw_data = requests.get(url).text
        location = raw_data.find("cse_token")
        token = raw_data[location + 13: location + 55]
        if len(token) < 10:
            raise CloseSpider("Unable to get cse token")
        return token

    def title_extractor(self, json_data):
        """
        Description    : This Function will parse json data for name, organisation and designation
        
        return         : name, organisation and designation
        json_data      : json data to parse
        """
        title = ""
        try:
            title = json_data["richSnippet"]["metatags"]["twitterTitle"].split("|")[0].split("-")
            title = [i.strip() for i in title]
        except:
            try:
                title_no_format = json_data["richSnippet"]["metatags"]["ogTitle"]
                title_no_format = re.split('[+,|]|profiles | LinkedIn|"', title_no_format)[0]
                if len(title_no_format) > 3:
                    title = title_no_format.split("-")
                else:
                    title = "NA"
            except Exception as e:
                self.logger.error(f"error on extracting title {e} -- {title}")
        try:
            if len(title) < 2 and type(title) == list:
                title = title[0].split("–")
            if len(title) < 2:
                name = title
                org, degs = "NA", "NA"
            elif len(title) == 2:
                name, org = title
                degs = "NA"
            elif len(title) == 3:
                name, degs, org = title
            else:
                name, degs, *rest = title
                org = "".join(rest)
            return name.strip(), org.strip(), degs.strip()
        except Exception as e:
            self.logger.error(f"error while title extraction {e}")
            return "", "", ""
