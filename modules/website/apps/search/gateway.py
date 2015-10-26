# -*- coding: utf-8 -*-

from website.apps.search.templatetags.template_additions import truncatechars
from website.apps.search.utils import timesince, Pagination, QueryParser

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings

from pyes import StringQuery, FilteredQuery, MatchAllFilter, MatchAllQuery, TermFilter, ORFilter, QueryFilter
from pyes import ES, GeoDistanceFilter, Search

import logging
import urllib2

logger = logging.getLogger('website.search.gateway')

class EmptyResults(object):
    total = 0

class ElasticSearch(object):
    def __init__(self, query):
        self.elastic = ES(settings.SEARCH_HOSTS)
        self.query = QueryParser(query)

    def search(self, index_type='job'):
        if not self.query.is_valid():
            self.results = EmptyResults()
            return

        where_filters = [ MatchAllFilter() ]

        if self.query.params['where']:
            where_filters= [ QueryFilter(StringQuery(self.query.get_where(), search_fields=['city'],\
                analyze_wildcard=True, default_operator="AND")) ]

        query = FilteredQuery(
            StringQuery(self.query.params['what'], search_fields=settings.SEARCH_WHAT_FIELDS, default_operator='AND', analyze_wildcard=True)\
                if self.query.params['what'] else MatchAllQuery(),
            ORFilter(self._get_geo_filters(where_filters))
        )

        facets_filter = []

        if self.query.params.has_key('company.facet') and len(self.query.params['company.facet']):
            facets_filter.append(TermFilter('company.facet', self.query.params['company.facet']))

        sorting = {'_score': {'order': 'desc' }}

        if self.query.params.has_key('sorting'):
            if self.query.params['sorting'] in ['score', 'published_date']:
                sorting = {self.query.params['sorting']: {'order': 'desc' }}

        query = Search(
            query, ORFilter(facets_filter) if len(facets_filter) else [],
            start=self.query.start_page(), size=settings.PAGINATION_PAGE_SIZE, sort=sorting
        )

        query.facet.add_term_facet(
            'company.facet',
            size=settings.SEARCH_FACETS_SIZE
        )

        self.results = self.elastic.search(query, settings.SEARCH_ALIASES, index_type)
        logger.info('Elastic query: %s\n' % str(query.to_search_json()))

    def get_results(self):
        data = []

        if self.results.total:
            for result in self.results.hits:
                item = {}

                if result.has_key('_source'):
                    item = result['_source']
                    del item['details_url']

                    if item.has_key('title'):
                        item['redirect_url'] = reverse('redirect', kwargs={
                            'slug'   : slugify(result['_source']['title']),
                            'source' : result['_source']['source'],
                            'job_id' : result['_id']
                        })

                    if item.has_key('published_date'):
                        item['published_date_ago'] = timesince(result['_source']['published_date']).encode('utf-8')

                    if item.has_key('summary'): item['summary'] = truncatechars(result['_source']['summary'], 350)
                    elif item['content']:       item['summary'] = truncatechars(result['_source']['content'], 350)

                    if item.has_key('image'):
                        item['image'] = '%s/job/thumbs/small/%s' % (settings.MEDIA_URL, item['image'])

                if len(item):
                    data.append(item)

        return data

    def get_facets(self):
        facets = {}

        if self.results.total:
            for facet in self.results.facets:
                if self.results.facets[facet].has_key('terms'):
                    facets[facet] = self.results.facets[facet]['terms']

            if facets.has_key('company.facet'):
                for item in facets['company.facet']:
                    if self.query.params.has_key('company.facet') and len(self.query.params['company.facet'])\
                        and self.query.params['company.facet'] == item['term']:
                            item['url'] = self._get_url({'company.facet': '', 'page': 1})
                            item['active'] = True
                    else:
                        item['url'] = self._get_url({'company.facet': item['term'], 'page': 1})

        return facets

    def list_pages(self):
        if self.results.total <= 0:
            return []

        pages = divmod(self.results.total, settings.PAGINATION_PAGE_SIZE)
        pages = pages[0] + 1 if pages[1] > 0 else pages[0]

        paginator = Pagination(self.query.params['page'], settings.PAGINATION_PAGE_SIZE, self.results.total)
        iterator = paginator.iter_pages(
            left_current  = settings.PAGINATION_CURRENT_LEFT,
            right_current = settings.PAGINATION_CURRENT_RIGHT,
            left_edge     = settings.PAGINATION_EDGE_LEFT,
            right_edge    = settings.PAGINATION_EDGE_RIGHT
        )

        return [{
            'page': page,
            'url': self._get_url({'page': page}),
            'selected': self.query.params['page'] == page
        } for page in iterator]

    def close(self):
        self.elastic.connection.close()

    def _get_geo_filters(self, filters=[]):
        for geo in self.query.get_geoquery():
            filters.append(GeoDistanceFilter(
                'pin.location',
                { 'lat' : geo[0], 'lon': geo[1] },
                settings.APP_GEO_CITIES_RANGE
            ))

        return filters

    def _get_url(self, data):
        params = self.query.params.copy()
        params.update(data)

        url = ''

        for key, value in params.items():
            url += '%s=%s&' % (key, urllib2.quote(unicode(value).encode('utf8')))

        return url[:-1]
