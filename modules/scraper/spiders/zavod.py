# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner
from scrapy.http import Request

from scraper.items import JobItem
from scraper.loaders import JobLoader
from scraper.spiders import BaseSpider

class ZavodSpider(BaseSpider):
    name = 'zavod'
    label = 'ZRSZ'
    allowed_domains = ['ess.gov.si']
    start_urls = ['http://www.ess.gov.si/iskalci_zaposlitve/prosta_delovna_mesta/seznam?q=1']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        next_page = hxs.select("//div[contains(@class, 'pagination')]/span/following-sibling::a[1]/@href").re(r"'(.*)','(.*)'")

        if next_page:
            yield Request(
                url=response.url,
                method='POST',
                headers= {
                    'content-type'     : 'application/x-www-form-urlencoded; charset=utf-8',
                    'x-requested-with' : 'XMLHttpRequest',
                    'x-microsoftajax'  : 'Delta=true'
                },
                body=self.build_formdata({
                    '__EVENTTARGET'  : next_page[0],
                    '__EVENTARGUMENT': next_page[1],
                }),
                callback=self.parse
            )

        for add in hxs.select("//div[@class='cc-gv']/table/tbody//tr"):
            name = add.select("td[1]/a/text()").extract_unquoted()
            company = add.select("td[2]/text()").extract_unquoted()

            if name and company:
                detail_url = add.select("td[1]/a/@href").extract()
                detail_url = self.get_base_url(response, detail_url[0])

                if detail_url:
                    item = JobItem()
                    item['title'] = name
                    item['company'] = company
                    item['published_date'] = add.select("td[3]/text()").extract_unquoted()
                    item['details_url'] = url_query_cleaner(detail_url, ('IDEPD'))
                    item['city'] = add.select("td[4]/text()").extract_unquoted()

                    yield Request(url=detail_url, callback=self.parse_job_detail, meta={'item': item})

    def parse_job_detail(self, response):
        hxs = HtmlXPathSelector(response)

        loader = JobLoader(JobItem())
        loader.add_item(response.request.meta['item'])
        loader.add_value('id', self.generate_id(response.url, ('IDEPD')))
        loader.add_value('source', self.name)
        loader.add_value('source_label', self.label)
        loader.add_value('summary', hxs.select("//div[@class='cc-gv']//tr/td[contains(text(),'Opis del in nalog')]/following-sibling::td[1]/text()").extract_unquoted())
        loader.add_value('content', response.body_as_unicode())

        yield loader.load_item()
