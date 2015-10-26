# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner
from scrapy.http import Request

from scraper.items import JobItem
from scraper.loaders import JobLoader
from scraper.spiders import BaseSpider

class MojedeloSpider(BaseSpider):
    name = 'mojedelo'
    label = 'MojeDelo.com'
    allowed_domains = ['mojedelo.com']
    start_urls = ['http://www.mojedelo.com/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        for link in hxs.select("//div[@id='workfields']/ul[@class='category-listing']//li/ul//li//a/@href"):
            yield Request(url=self.get_base_url(response, link.extract()), 
                callback=self.parse_job
            )

    def parse_job(self, response):
        hxs = HtmlXPathSelector(response)
        next_page = hxs.select("//div[@class='PagedList-pager']//ul/li[contains(@class, 'PagedList-currentPage')]/following-sibling::li[1]/a/@href").extract()
        
        if next_page:
            next_page = self.get_base_url(response, next_page[0])
            
            if next_page != self.get_base_url(response, response.request.url):
                yield Request(url=next_page, callback=self.parse_job)
          
        category = hxs.select("//form[@id='searchForm']//select[@name='wfid']/option[@selected='selected']/text()").extract()      
        informations = hxs.select("//table[@class='job-add-listing']//tr//div[@class='job-add-item-inner']")
        
        for information in informations:
            name    = information.select("h2/a/text()").extract()
            company = information.select("p[3]/strong/text()").extract()

            if name and company:                
                detail_url = information.select("h2/a/@href").extract()
                detail_url = self.get_base_url(response, detail_url[0])
                
                if detail_url:
                    images_url = information.select("div[contains(@class,'city-logo')]/img/@src").extract()
                    item = JobItem()
                    
                    item['title'] = name
                    item['company'] = company
                    item['category'] = category
                    item['summary'] = information.select("p[2]/text()").extract()
                    item['city'] = information.select("p[1]/text()").extract()
                    item['details_url'] = url_query_cleaner(detail_url)
                    item['published_date'] = information.select("div[contains(@class,'city-logo')]/div/text()").extract()
                    
                    if images_url:
                        item.load_image(self.get_base_url(response, images_url[0]))
                
                    yield Request(url=detail_url, callback=self.parse_job_detail, meta={'item': item})
                    
    def parse_job_detail(self, response):       
        loader = JobLoader(JobItem())
        loader.add_item(response.request.meta['item'])
        loader.add_value('id', self.generate_id(response.url))
        loader.add_value('source', self.name)
        loader.add_value('source_label', self.label)
        loader.add_value('content', response.body_as_unicode())

        yield loader.load_item()
