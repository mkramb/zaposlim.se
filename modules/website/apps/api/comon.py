# -*- coding: utf-8 -*-

from website.apps.search.models import City, Log
from website.apps.common.models import Page

from piston.handler import BaseHandler
from piston.utils import rc

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.handlers.wsgi import WSGIRequest

from pyes import ES, GeoDistanceFilter, FilteredQuery, MatchAllQuery
from pyes import QueryFilter, StringQuery, ORFilter

import threading

class AutocompleteHandler(BaseHandler):
    allowed_methods = ('GET',)

    handlers = {
        'where' : lambda self, query: self._complete_where(query)
    }

    def read(self, request, param):
        if param not in self.handlers.keys():
            return rc.BAD_REQUEST

        return self.handlers[param](self, request.GET.get('q', None))

    def _complete_where(self, query):
        if query:
            query = query.strip()
            cities = City.objects.filter(name__istartswith=query)

            return {
                'response' :  {
                    'numFound' : len(cities),
                    'docs'     : [ {'term': city.name} for city in cities ]
                }
            }

        return rc.NOT_FOUND

class StatsHandler(BaseHandler):
    allowed_methods = ('GET',)

    handlers = {
        'searches': lambda self, request: self._get_searches(request),
        'queries': lambda self, request: self._get_queries(request),
        'geo': lambda self, request: self._calculate_geo(request),
    }

    def read(self, request, param):
        if param not in self.handlers.keys():
            return rc.BAD_REQUEST

        return self.handlers[param](self, request)

    def _get_searches(self, request):
        if not (request or request is WSGIRequest):
            return rc.BAD_REQUEST

        query = request.GET.get('query', None)
        columns = settings.APP_SEARCHES_MORE_COLUMNS
        searches = {}

        if not query:
            return rc.BAD_REQUEST

        if query == 'top':
            searches_top = Log.objects.top_items(settings.APP_SEARCHES_MORE_TOP)
            searches = self._process_colums(searches_top, columns)
        elif query == 'latest':
            searches_latest = Log.objects.last_items(settings.APP_SEARCHES_MORE_LAST)
            searches = self._process_colums(searches_latest, columns)

        return searches

    def _get_queries(self, request):
        searches = { 'top': [], 'latest': [] }

        for top in Log.objects.top_items():
            searches['top'].append({
                'name': top.what,
                'name_short': top.what_short
            })

        for last in Log.objects.last_items():
            searches['latest'].append({
                'name': last.what,
                'name_short': last.what_short
            })

        return searches

    def _calculate_geo(self, request):
        cities = cache.get('website.cities')

        if not cities:
            elastic = ES(settings.SEARCH_HOSTS)
            geo = []

            for city, location in settings.APP_GEO_CITIES.items():
                filters = [
                    QueryFilter(StringQuery(city, search_fields=['city'], analyze_wildcard=True, default_operator="AND")),
                    GeoDistanceFilter('pin.location', { 'lat' : location[0], 'lon': location[1] }, settings.APP_GEO_CITIES_RANGE)
                ]

                geo.append((city,
                    elastic.count(FilteredQuery(
                        MatchAllQuery(),
                        ORFilter(filters)
                    ), settings.SEARCH_ALIASES)['count'],
                    { 'lat' : location[0], 'lon': location[1] }
                ))

            elastic.connection.close()

            data = []
            start_radius, max_radius = (5000, 10000) # 16km radius
            quotient = None

            for city in sorted(geo, key=lambda student: student[1], reverse=True):
                if city[1] > 0:
                    if not quotient:
                        quotient = int(max_radius / city[1])

                    radius = city[1] * quotient + start_radius
                    data.append((radius,) + city)

            cities = data
            cache.set('website.cities', cities)

        return cities

    def _process_colums(self, what, columns):
        columns_count = len(columns)
        rows = {}

        for top in xrange(0, len(what), columns_count):
            counter = 0

            for result in what[top:top+columns_count]:
                key = columns[counter]

                if not rows.has_key(key):
                    rows[key] = []

                rows[key].append({
                    'name': result.what,
                    'name_short': result.what_short
                })

                counter += 1

        return rows

class PagesHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Page

    def read(self, request):
        try:
            page = Page.objects.get(slug=request.GET['slug'])

            return {
                'title': page.title,
                'content': page.content
            }
        except Page.DoesNotExist:
            return rc.NOT_FOUND

class ContactHandler(BaseHandler):
    allowed_methods = ('POST',)

    def create(self, request):
        form_data = {}

        for value in request.data["data"]:
            form_data[value['name']] = value['value']

        if form_data['email'] and form_data['subject'] and form_data['name'] and form_data['message']:
            subject = "%s from %s" % (form_data['subject'], form_data['name'])
            message = "%s\n\n%s" % (form_data['email'], form_data['message'])

            recipients = zip(*settings.ADMINS)[1]
            from_mail = form_data['email']

            t = threading.Thread(
                target=send_mail,
                args=[subject, message, from_mail, recipients],
                kwargs={'fail_silently': True}
            )

            t.setDaemon(True)
            t.start()

            return { 'success': True }
        return rc.BAD_REQUEST
