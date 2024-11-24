import asyncio
import json

import aiohttp
import random
from scrapy.exceptions import NotConfigured, CloseSpider

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
        self.SCRAPERAPI_RENDER = settings.get('SCRAPERAPI_RENDER', False)
        self.SCRAPERAPI_PREMIUM = settings.get('SCRAPERAPI_PREMIUM', False)
        self.SCRAPERAPI_COUNTRY_CODE = settings.get('SCRAPERAPI_COUNTRY_CODE', '')

        self.SCRAPERAPI_CLIENT = None
        loop = asyncio.get_event_loop()
        self.live_apikeys = loop.run_until_complete(self.get_liveapi())
        if len(self.live_apikeys) < 2:
            raise CloseSpider("Exhausted all scraper api, please add new api keys")

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_request(self, request, spider):
        if 'api.scraperapi.com' not in request.url:
            log.info("Process request...")
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
        return

    async def fetch(self, session, url):
        async with session.get(url) as response:
            # logging.info(response.json())
            return await response.read()
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

    async def get_liveapi(self):
        live_apikeys = []
        logging.debug("opened spider")
        tasks = []
        async with aiohttp.ClientSession() as session:
            for token in self.SCRAPERAPI_KEY:
                url = "http://api.scraperapi.com/account?api_key={}".format(token)
                tasks.append(self.fetch(session, url))
            responses = await asyncio.gather(*tasks)
            for res in responses:
                try:
                    # logging.debug(res)
                    r = json.loads(res)
                    response = r["requestCount"]
                    # logging.debug(response)
                    if response < 1000:
                        live_apikeys.append(token)
                except Exception as e:
                    logging.error("error on token {} -- {}".format(token, e))

        logging.debug(f"{len(live_apikeys)} keys alive")
        return live_apikeys
