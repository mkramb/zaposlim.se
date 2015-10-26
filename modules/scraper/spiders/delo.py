from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner, urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy.http import Request

from scraper.items import JobItem
from scraper.loaders import JobLoader
from scraper.spiders import BaseSpider

class DeloSpider(BaseSpider):
    name = 'delo'
    label = 'Delo.si zaposlitev'
    allowed_domains = ['zaposlitev.delo.si']
    start_urls = ['http://zaposlitev.delo.si/index.php']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        search_url = urljoin_rfc(get_base_url(response), "iskanje.php?najdi=spl&vse=1&izob=0&kraj=0&akcija=POTRDI&SZ=")
        
        for category in hxs.select("//select[@name='pod[]']/option"):
            yield Request(
                url=search_url + "&pod[]=%s" % category.select("@value").extract()[0], 
                meta={'category' : category.select("text()").extract()}, callback=self.parse_jobs, dont_filter=True
            )

    def parse_jobs(self, response):
        hxs = HtmlXPathSelector(response)
        
        for add in hxs.select("//form[@name='zadetkov']/../table[2]//tr[position() > 2]/td[not(@colspan)]/.."):
            yield Request(
                url=self.get_base_url(response, add.select("td[5]/a/@href").extract()[0]), 
                meta = {'category' : response.request.meta['category']}, callback=self.parse_job_detail
            )
            
    def parse_job_detail(self, response):        
        hxs = HtmlXPathSelector(response)
        
        title = hxs.select("//span[@class='header']/text()").extract_unquoted()       
        company = hxs.select("//span[@class='fontblacklarge']/b/text()").extract_unquoted()   
             
        if title and company: 
            city = hxs.select("//span[@class='fontblacklarge']/b[2]/text()").extract_unquoted()
            category = response.request.meta['category']        
            published_date = hxs.select("//span[@class='fontblacklarge']/../../following-sibling::tr[2]/td/b/text()").extract_unquoted()
            
            item=JobItem()
            images_url = hxs.select("//span[@class='fontblacklarge']/../following-sibling::td[2]/img/@src").extract()        
            
            if images_url:
                item.load_image(self.get_base_url(response, images_url[0]))
            
            loader = JobLoader(item)
            loader.add_value('title', title)
            loader.add_value('company', company)
            loader.add_value('category', category)
            loader.add_value('city', city)
            loader.add_value('details_url', url_query_cleaner(response.url, ('najdi', 'id')))
            loader.add_value('published_date', published_date)
            loader.add_value('id', self.generate_id(response.url, ('najdi', 'id')))
            loader.add_value('content', response.body_as_unicode())
            loader.add_value('source', self.name)
            loader.add_value('source_label', self.label)
            
            yield loader.load_item()
