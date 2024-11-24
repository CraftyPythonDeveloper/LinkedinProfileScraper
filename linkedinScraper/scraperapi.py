import json
from urllib.parse import urlparse
import random

import requests
from scrapy.exceptions import NotConfigured, CloseSpider
from sqlalchemy import create_engine

try:
    from scraper_api import ScraperAPIClient
except:
    pass

import logging

log = logging.getLogger('scrapyx.scraperapi')


class ScraperApiProxyMiddleware(object):
    def __init__(self, settings):
        if not settings.getbool('SCRAPERAPI_ENABLED', True):
            raise NotConfigured

        self.SCRAPERAPI_KEY = settings.get('SCRAPERAPI_KEY', '')
        logging.debug(self.SCRAPERAPI_KEY)
        self.SCRAPERAPI_RENDER = settings.get('SCRAPERAPI_RENDER', False)
        self.SCRAPERAPI_PREMIUM = settings.get('SCRAPERAPI_PREMIUM', False)
        self.SCRAPERAPI_COUNTRY_CODE = settings.get('SCRAPERAPI_COUNTRY_CODE', '')

        self.SCRAPERAPI_CLIENT = None
        self.live_apikeys = self.get_liveapi()
        self.is_herkou = False
        # self.heroku_proxy = settings.get('HEROKU_PROXY', False)
        if len(self.live_apikeys) < 2:
            proxy_settings = settings.get("PROXY_SETTINGS")
            self.proxy_route = proxy_settings.get("PROXY_ROUTE", "get?url=")
            engine = create_engine(proxy_settings.get("DB_CONN"))
            proxy_conn = engine.connect()
            column_name = proxy_settings.get('COLUMN_NAME')
            self.heroku_proxy_urls = proxy_conn.execute(f"select {column_name} from {proxy_settings.get('TABLE_NAME')}").fetchall()
            self.heroku_proxy_urls = [i[column_name] for i in self.heroku_proxy_urls]
            if not self.heroku_proxy_urls:
                raise CloseSpider("Exhausted all scraper api and no heroku proxies, please add new api keys")
            self.is_herkou = True

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_request(self, request, spider):
        if 'api.scraperapi.com' not in request.url:
            # log.info("Process request...")
            if not self.is_herkou:
                try:
                    self.SCRAPERAPI_CLIENT = ScraperAPIClient(random.choice(self.live_apikeys))
                # 403 used all api
                except:
                    raise NotConfigured
                new_url = self.SCRAPERAPI_CLIENT.scrapyGet(url=request.url,
                                                           render=self.SCRAPERAPI_RENDER,
                                                           country_code=self.SCRAPERAPI_COUNTRY_CODE,
                                                           premium=self.SCRAPERAPI_PREMIUM)

                log.info("New url: {}".format(new_url))
                return request.replace(url=new_url)
            random_heroku_proxy = random.choice(self.heroku_proxy_urls)
            if "heroku" not in request.url:
                new_url = f"{random_heroku_proxy}/{self.proxy_route}{request.url}"
                log.info("New url: {}".format(new_url))
                return request.replace(url=new_url)
            return
        return

    def fetch(self, url):
        response = requests.get(url)
        # logging.info(response.json())
        return response.text

    #
    # def get_liveapi(self):
    #     live_apikeys = []
    #     logging.debug("opened spider")
    #     for token in self.SCRAPERAPI_KEY:
    #         url = "http://api.scraperapi.com/account?api_key={}".format(token)
    #         try:
    #             response = requests.get(url).json()["requestCount"]
    #             #         print(response)
    #             if response < 1000:
    #                 live_apikeys.append(token)
    #         except Exception as e:
    #             logging.error("error on token {} -- {}".format(token, e))
    #
    #     logging.debug(f"{len(live_apikeys)} keys alive")
    #     return live_apikeys

    def get_liveapi(self):
        live_apikeys = []
        logging.debug("opened spider")
        for token in self.SCRAPERAPI_KEY:
            # logging.debug(token)
            url = "http://api.scraperapi.com/account?api_key={}".format(token)
            res = self.fetch(url)
            # logging.debug(res)
            try:
                r = json.loads(res)
                response = r["requestCount"]
                if response < 200:
                    live_apikeys.append(token)
                    logging.debug(f"Key {token} used {response} requests")
            except Exception as e:
                logging.error("error on token {} -- {}".format(token, e))
        logging.debug(f"{len(live_apikeys)} keys alive")
        return live_apikeys
