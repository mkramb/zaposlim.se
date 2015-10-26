# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner
from scrapy.http import Request, FormRequest

from scraper.items import JobItem
from scraper.loaders import JobLoader
from scraper.spiders import BaseSpider

class BorzadelaSpider(BaseSpider):
    name = 'borzadela'
    label = 'BorzaDela.si'
    allowed_domains = ['borzadela.najdi.si']
    start_urls = ['http://borzadela.najdi.si/']

    def parse(self, response):
        yield FormRequest(url=u'http://borzadela.najdi.si/aktualna-prosta-delovna-mesta',
            formdata={'jobemploymenttype': '4'}, callback=self.parse_category, dont_filter=True
        )

        yield FormRequest(url=u'http://borzadela.najdi.si/aktualna-prosta-delovna-mesta',
            formdata={'jobadtype': '1'}, callback=self.parse_category, dont_filter=True
        )

    def parse_category(self, response):
        hxs = HtmlXPathSelector(response)
        next_page = hxs.select("//li[@class='li-navigation-selected']/following-sibling::li[1]/a/text()").extract_unquoted()

        if next_page:
            yield FormRequest.from_response(response, formname='jobsearchform',
                formdata={'page': next_page}, callback=self.parse_category, dont_filter=True
            )

        for add in hxs.select("//li[@class='jobsearchmain']/div[@class='addiv' or @class='addivnone']"):
            yield Request(url=add.select("a/@href").extract()[0], callback=self.parse_job_detail, dont_filter=True)

    def parse_job_detail(self, response):
        hxs = HtmlXPathSelector(response)

        title = hxs.select("//div[@id='businessmyaccountjobadpreviewmain']/div/font/text()").extract_unquoted()
        company = hxs.select("//li[@class='propertiesleft' and contains(text(),'Podjetje:')]/following-sibling::li/text()").extract_unquoted()

        if title and company:
            city = hxs.select("//li[@class='propertiesleft' and contains(text(),'Regija in kraj dela:')]/following-sibling::li/text()").extract_unquoted()
            category = hxs.select(u"//li[@class='propertiesleft2' and contains(text(),'Področje dela:')]/following-sibling::li/text()".encode('utf-8')).extract_unquoted()
            images_url = hxs.select("//img[@id='mainimage']/@src").extract()
            item=JobItem()

            if images_url:
                item.load_image(self.get_base_url(response, images_url[0]))

            loader = JobLoader(item)
            loader.add_value('title', title)
            loader.add_value('company', company)
            loader.add_value('category', category)
            loader.add_value('city', city)
            loader.add_value('details_url', url_query_cleaner(response.url))
            loader.add_value('published_date', hxs.select("//li[@class='dates']/text()").re(r".*:\s+(.*)"))
            loader.add_value('id', self.generate_id(response.url))
            loader.add_value('content', response.body_as_unicode())
            loader.add_value('source', self.name)
            loader.add_value('source_label', self.label)

            yield loader.load_item()
