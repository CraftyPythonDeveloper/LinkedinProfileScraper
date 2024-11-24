# Scrapy settings for linkedinScraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from urllib.parse import quote_plus
BOT_NAME = 'linkedinScraper'

SPIDER_MODULES = ['linkedinScraper.spiders']
NEWSPIDER_MODULE = 'linkedinScraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'linkedinScraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'linkedinScraper.middlewares.LinkedinscraperSpiderMiddleware': 543,
# }


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'linkedinScraper.middlewares.LinkedinscraperDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'linkedinScraper.pipelines.LinkedinscraperPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Activate the middleware
SCRAPERAPI_ENABLED = False

# The API key
SCRAPERAPI_KEY = []

# JS Redering
SCRAPERAPI_RENDER = False

# Premium account
SCRAPERAPI_PREMIUM = False

# Geographic Location
SCRAPERAPI_COUNTRY_CODE = ''  # 'US', 'UK', ...

USER_AGENT = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 '
              'Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 '
              'Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/98.0.4758.109 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/98.0.4758.109 Safari/537.36 '
              'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
              'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 '
              'Safari/605.1.15 ',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
              'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 '
              'Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 '
              'Safari/537.36 Edg/98.0.1108.62 '
              ]

MAX_PAGE_CRAWL = 10

CSE_API_URL = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com" \
                       "&cselibv=921554e23151c152&cx=011658049436509675749:gkuaxghjf5u&q={query}&safe=off&cse_tok={" \
                       "cse_token}&sort=&exp=csqr,cc&callback=google.search.cse.api{random_number}&start={page_number}"

CSE_TOKEN_URL = "https://cse.google.com/cse.js?cx=011658049436509675749:gkuaxghjf5u"

DOWNLOADER_MIDDLEWARES = {
    'linkedinScraper.scraperapi.ScraperApiProxyMiddleware': 610
    # 'linkedinScraper.Hproxy.HerokuProxyMiddleware': 610
}

# HEROKU_ENABLED = True
# HEROKU_URL_SPLIT_AT = "get?url="
# HEROKU_PROXY = ["https://limitless-scrubland-28862.herokuapp.com",
#                 "https://vast-headland-82536.herokuapp.com",
#                 "https://polar-tor-11817.herokuapp.com",
#                 "https://sleepy-eyrie-91467.herokuapp.com",
#                 "https://still-temple-94613.herokuapp.com"]

PROXY_SETTINGS = {
    "DB_CONN": "sqlite:///linkedin.db",
    "TABLE_NAME": "proxy_servers",
    "COLUMN_NAME": "proxy_url",
    "PROXY_NAME": "heroku",
    "PROXY_ROUTE": "get?url="
}


RETRY_TIMES = 3

# LOG_FILE = "scrapy.log"

SQL_CONNECTION_STRING = "sqlite:///linkedin.db"