# -*- coding: utf-8 -*-

from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import signals, log

from scraper.items import JobItem
from website.apps.common.models import Data
from website.apps.search.tasks.process import ProcessSpiderData

from django.db import transaction
from datetime import datetime, timedelta

import hashlib
import os

class SkipDuplicatesPipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.duplicates[spider] = set()

    def spider_closed(self, spider):
        del self.duplicates[spider]

    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            if item['id'] in self.duplicates[spider]:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.duplicates[spider].add(item['id'])
                return item

class LimitByDatePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            if item['published_date'] < datetime.now() - timedelta(days=settings['JOB_DATE_EXPIRES']):
                raise DropItem("Items published date is too old: %s" % item)
            return item

class SavePipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        Data.objects.filter(name=spider.name).delete()
        self.spider_data = Data(name=spider.name)
        self.spider_data.source = [];

    def spider_closed(self, spider):
        self.spider_data.save()

        transaction.commit()
        ProcessSpiderData.delay(spider.name)

        os.system('chmod -R 755 %s/full' % settings['IMAGES_STORE'])
        os.system('chmod -R 755 %s/thumbs' % settings['IMAGES_STORE'])

    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            data = dict(item)

            if data.has_key('images') and data['images']:
                data['image'] = "%s.jpg" % hashlib.sha1(data['images'][0]['url']).hexdigest()
                del data['image_urls']
                del data['images']

            self.spider_data.source.append(data)

            log.msg('Saved source "%s", document id: "%s"' %
                (spider.name, data['id']), level=log.INFO
            )

            return item
