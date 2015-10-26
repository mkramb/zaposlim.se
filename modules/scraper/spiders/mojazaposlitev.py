# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner
from scrapy.http import Request

from scraper.items import JobItem
from scraper.loaders import JobLoader
from scraper.spiders import BaseSpider

class MojazaposlitevSpider(BaseSpider):
    name = 'mojazaposlitev'
    label = 'MojaZaposlitev.si'
    allowed_domains = ['mojazaposlitev.si']
    start_urls = ['http://www.mojazaposlitev.si']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        titles = hxs.select("//div[@id='podrocja-dela']//li/a/text()")
        links = hxs.select("//div[@id='podrocja-dela']//li/a/@href")

        for title, link in zip(titles, links):
            yield Request(
                url=self.get_base_url(response, link.extract()),
                callback=self.parse_job, meta={'category': title.extract_unquoted()}
            )

    def parse_job(self, response):
        hxs = HtmlXPathSelector(response)
        next_page = hxs.select("//ul[@class='pagination']/li[@class='selected']//following-sibling::li[1]/a/@href").extract()

        if next_page:
            next_page = self.get_base_url(response, next_page[0])
            if next_page != self.get_base_url(response, response.request.url):
                yield Request(url=next_page, callback=self.parse_job, meta={'category': response.request.meta['category']})

        for job in hxs.select("//ul[@id='newJobs']/li"):
            name = job.select("p[@class='jobTitle']/a/text()").extract_unquoted()
            company = job.select("strong/text()").extract_unquoted()

            if name and company:
                detail_url = job.select("p[@class='jobTitle']/a/@href").extract()
                detail_url = self.get_base_url(response, detail_url[0])

                if detail_url:
                    images_url = job.select("div[@class='jobImgDiv']/img/@src").extract()
                    item = JobItem()

                    item['title'] = name
                    item['company'] = company
                    item['category'] = response.request.meta['category']
                    item['summary'] =  job.select("p[2]/text()").extract_unquoted()
                    item['details_url'] = url_query_cleaner(detail_url)
                    item['published_date'] = job.select("span[1]/text()").re(r".*:\s(.*)")

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
