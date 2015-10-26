# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os
from random import choice

# project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# logging
LOG_ENABLED = True
LOG_LEVEL = 'ERROR'
LOG_FILE = os.path.join(PROJECT_ROOT, 'scraper.log')

# global settings
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
DEFAULT_ITEM_CLASS = 'scraper.items.JobItem'

USER_AGENTS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
]

USER_AGENT = choice(USER_AGENTS_LIST)

ITEM_PIPELINES = [
    'scraper.pipelines.SkipDuplicatesPipeline',
    'scraper.pipelines.LimitByDatePipeline',
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'scraper.pipelines.SavePipeline',
]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':110,
    'scraper.middlewares.TorProxyMiddleware': 740,
}

TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = False
COOKIES_ENABLED = True

# email settings
MAIL_FROM = 'mail@zaposlim.se'
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USER = 'mail@zaposlim.se'
MAIL_PASS = 'delampridno'

# crawling settings
REDIRECT_MAX_TIMES = 4
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.10

MEMUSAGE_ENABLED = False
MEMUSAGE_LIMIT_MB = 1024
MEMUSAGE_NOTIFY_MAIL = ['mitja.kramberger@gmail.com']
MEMUSAGE_REPORT = False

# item settings - local
JOB_DATE_EXPIRES = 31 # days

# images settings
IMAGES_STORE = os.path.join(PROJECT_ROOT, '../website/media/job')
IMAGES_MIN_WIDTH = 32
IMAGES_MIN_HEIGHT = 32
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
    'small': (100, 65),
}

# init django enviroment
from scraper.utils import setup_django_env
setup_django_env(os.path.join(PROJECT_ROOT, '../website/'))

try:
    from settings_local import *
except ImportError:
    pass
