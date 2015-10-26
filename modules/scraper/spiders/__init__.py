from scrapy.contrib.spiders import CrawlSpider
from scrapy.utils.url import urljoin_rfc, url_query_cleaner
from scrapy.utils.response import get_base_url
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

import hashlib

class BaseSpider(CrawlSpider):
    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)
    
    def generate_id(self, detail_url, parameterlist=()):
        detail_url = url_query_cleaner(detail_url, parameterlist)
        detail_url = ''.join([self.name, detail_url]).encode('utf-8')
        
        return hashlib.md5(detail_url).hexdigest()
    
    def get_base_url(self, response, url):
        return urljoin_rfc(get_base_url(response), url)
            
    def build_formdata(self, formdata):
        return '&'.join(['%s=%s' % (key, data) for key, data in formdata.items()])
