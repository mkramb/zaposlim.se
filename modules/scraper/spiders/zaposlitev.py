# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner
from scrapy.http import FormRequest, Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy.project import crawler
from scrapy import signals

from scraper.items import JobItem
from scraper.loaders import JobLoader
from scraper.spiders import BaseSpider

class ZaposlitevSpider(BaseSpider):
    name = 'zaposlitev'
    label = 'Zaposlitev.net'
    allowed_domains = ['zaposlitev.net']
    start_urls = ['http://www.zaposlitev.net']
    categories = []

    def __init__(self, *a, **kw):
        super(ZaposlitevSpider, self).__init__(*a, **kw)
        dispatcher.connect(self.spider_idle, signals.spider_idle)

    def spider_idle(spider):
        if len(spider.categories):
            crawler.engine.crawl(spider.categories.pop(), spider)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        for category in hxs.select("//input[@type='checkbox' and contains(@class, 'iskalnik_kriteriji_tip_sektor')]/@value"):
            self.categories.append(FormRequest.from_response(response,
                formdata={ 'search[sektor_skupina][]': category.extract() },
                callback=self.parse_job, dont_filter=True
            ))

        yield self.categories.pop()

    def parse_job(self, response):
        hxs = HtmlXPathSelector(response)
        next_page = hxs.select("//span[@class='stevilke']/a[contains(@class, 'active')]/following-sibling::a[1]/@href").extract()

        if next_page:
            next_page = self.get_base_url(response, next_page[0])
            if next_page != self.get_base_url(response, response.request.url):
                yield Request(url=next_page, callback=self.parse_job)

        category = hxs.select(
            "//input[@type='checkbox' and contains(@class, 'iskalnik_kriteriji_tip_sektor') and @checked]" +
            "//following-sibling::label[1]/text()"
        ).extract_unquoted()

        for job in hxs.select("//tr[@class='bg_oglas_dm']"):
            name = job.select("td[@class='ena']/div/a/b/text()").extract_unquoted()
            company = job.select("td[@class='dva']/a/text()").extract_unquoted()

            if name and company:
                detail_url = job.select("td[@class='ena']/div/a/@href").extract()
                detail_url = self.get_base_url(response, detail_url[0])

                if detail_url:
                    images_url = job.select("td[@class='stiri']//img/@src").extract()
                    item = JobItem()

                    item['title'] = name
                    item['company'] = company
                    item['category'] = category
                    item['city'] = job.select("td[@class='tri']/a/text()").extract_unquoted()
                    item['details_url'] = url_query_cleaner(detail_url)
                    item['published_date'] = job.select("td[@class='stiri']//div[2]/text()").re(r"\s+(\d{2}.\d{2}.\d{4})\s+")

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
