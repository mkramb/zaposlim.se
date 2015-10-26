# -*- coding: utf-8 -*-

from website.apps.common.models import Data, DataBackup
from website.apps.common.fields import JSONEncoder
from website.apps.search.models import City
from website.apps.search.mapping import mapping

from celery.task import Task
from celery.registry import tasks

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.simplejson import dumps
from django.core.cache import cache
from django.conf import settings

from pyes.exceptions import ElasticSearchException
from pyes import ES

from java import JavaInterface
from geopy import geocoders
import jpype

import binascii
import time
import bz2
import re

normalize_spaces = re.compile(' +')
remove_braces = re.compile('\(.*\)')
remove_none_chars = re.compile('^[^a-zA-Z0-9._]+$')

class ProcessSpiderData(Task):
    def run(self, spider_name):
        cities = []
        backup_source = []
        backup_created_date = None

        self.elastic = ES(settings.SEARCH_HOSTS, timeout=22.0, bulk_size=1500)
        java = JavaInterface()

        self.extractor = java.ArticleSentencesExtractor.INSTANCE
        self.logger = ProcessSpiderData.get_logger()

        spider = Data.objects.get(name=spider_name)
        source = spider.source

        if spider and len(source):
            backup_created_date = spider.created_date
            index_new = '%s_%d' % (spider.name, int(time.time()))

            # create new index (not connected to alias)
            self.elastic.create_index(index_new)
            self.elastic.put_mapping('job', {'job':{'properties':mapping}}, index_new)

            for item in source:
                item = self._process_content(item)
                item = self._get_location(item)

                if item.has_key('city'):
                    cities.append(item['city'])

                self._create_index(index_new, item)
                backup_source.append(item)

            # save new index (in bulk)
            self.elastic.force_bulk()

            # create alias
            indices_old = self.elastic.get_alias(spider.name)
            self.elastic.set_alias(spider.name, [index_new])

            # delete all indices
            for index in indices_old:
                self.elastic.delete_index_if_exists(index)

            # optimize
            self.elastic.optimize(index_new, refresh=True)

        # save backup (currently processed data)
        if len(backup_source) and backup_created_date:
            self._process_cities(set(cities), spider_name)
            cache.clear()

            obj = DataBackup.objects.get_or_create(
                name=spider_name,
                created_date=backup_created_date
            )

            obj[0].source = binascii.hexlify(bz2.compress(
                JSONEncoder().encode(backup_source)
            ))

            obj[0].save()

        # force java & ES garbage collection
        self.elastic.connection.close()
        del self.extractor
        del java

        return True

    def _process_content(self, item):
        if len(item['content']):
            item['content'] = self.extractor.getText(jpype.JString(item['content']))
        return item

    def _get_location(self, item):
        if not item.has_key('city'):
            return item

        try:
            geo = geocoders.GeoNames()
            places = geo.geocode(item['city'].encode('utf-8'), exactly_one=False)

            if places:
                place, (lat, lon) = places[0] if isinstance(places, list) else places
                if place: item['pin'] = {
                    'location': { 'lat': lat, 'lon': lon }
                 }
        except: pass
        return item

    def _create_index(self, index, item):
        id = item['id']
        del item['id']

        try:
            self.elastic.get(index, 'job', id)
        except ElasticSearchException:
            self.elastic.index(
                dumps(item, cls=DjangoJSONEncoder),
                index, 'job', id, bulk=True
            )

    def _process_cities(self, cities, spider_name):
        cities_current = City.objects.filter(indices__contains='"%s"' % spider_name)

        # save lists of saved cities
        cities_old_single = [ city.name for city in cities_current if city.indices and spider_name in city.indices and len(city.indices) == 1 ]
        cities_old_multi = [ city.name for city in cities_current if city.indices and spider_name in city.indices and len(city.indices) > 1 ]

        for city in cities:
            city = unicode(city.strip().lower())
            city = normalize_spaces.sub(' ', city)
            city = remove_braces.sub('', city)

            city_clean = [remove_none_chars.sub('', word) for word in city.split(' ')]
            city_clean = ' '.join(filter(None, city_clean))

            city, created = City.objects.get_or_create(name = city_clean[:255])

            if created:
                city.indices = [spider_name]
            else:
                city.indices.append(spider_name)
                city.indices = list(set(city.indices))

            city.save()

            if city.name in cities_old_single: cities_old_single.remove(city.name)
            if city.name in cities_old_multi: cities_old_multi.remove(city.name)

        # remove unlinked citie
        City.objects.filter(name__in=cities_old_single).delete()

        for item in City.objects.filter(name__in=cities_old_multi):
            if spider_name in item.indices:
                item.indices.remove(spider_name)
                item.save()

tasks.register(ProcessSpiderData)
