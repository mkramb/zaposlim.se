# -*- coding: utf-8 -*-

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join

from datetime import datetime, timedelta
import re

class StripJoin(Join):
    def __call__(self, values):
        return super(StripJoin, self).__call__([x.strip() for x in values])

class ConvertToDate(object):
    def __init__(self, format=u'%d.%m.%Y'):
        self.format = format

    def __call__(self, values):
        for value in values:
            try:
                value = '.'.join([ part if len(part) >= 2 else ''.join(['0',part]) for part in value.split('.')])
                return datetime.strptime(value, self.format)
            except:
                if value.strip().lower() == u'včeraj':
                    return datetime.now() - timedelta(1)
                return datetime.now()

class CleanContent(Join):
    def __call__(self, values):
        for value in values:
            return ''.join([each.capitalize() for each in re.split('([.!?] +)', value)]).strip()

class RemoveNumbers(Join):
    def __call__(self, values):
        for value in values:
            return re.sub("\d+", "", value).strip()

class BaseLoader(ItemLoader):
    def add_item(self, item):
        for key, value in item.items():
            if key == 'image_urls' and len(value) > 0:
                self.item['image_urls'] = value
            else:
                self.add_value(key, value)

class JobLoader(BaseLoader):
    default_input_processor = StripJoin()
    default_output_processor = StripJoin()

    city_out = RemoveNumbers()
    title_out = CleanContent()
    published_date_out = ConvertToDate()

    company_out = CleanContent()
    summary_out = CleanContent()
