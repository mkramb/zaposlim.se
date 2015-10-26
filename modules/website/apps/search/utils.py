from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from math import ceil
from datetime import datetime
import re

class QueryParser():
    params = {
        'what': '',
        'where': '',
        'page': 1,
        'sorting': '_score',
    }

    normalize = re.compile(' +')
    special_chars = re.compile('\s*(\*|\+|\-|OR|AND)\s*')

    operators = re.compile('\s+OR\s+|\s+AND\s+')
    operators_included = re.compile('\s+(OR)\s+|\s+(AND)\s+')

    def __init__(self, query):
        self.params = dict(self.params, **query)

        if self.params['page']:
            self.params['page'] = self.params['page'] if self.params['page'] else 1
            self.params['page'] = int(self.params['page']) if int(self.params['page']) > 0 else 1

        if not query.has_key('company.facet') or not len(query['company.facet']):
            if self.params.has_key('company.facet'): del self.params['company.facet']

        self.params['what'] = self._clean_query(self.params['what'])
        self.params['where'] = self._clean_query(self.params['where'], only_or=True)

    def is_valid(self):
        if (self.params['what'] and self.params['what'].find('-') != 0) or\
          (self.params['where'] and self.params['where'].find('-') != 0):
            return True

    def start_page(self):
        selectedPage = int(self.params['page']) - 1
        selectedPage = selectedPage if selectedPage >= 0 else 0

        return selectedPage * settings.PAGINATION_PAGE_SIZE

    def get_where(self):
        params = self.operators_included.split(self.params['where'])
        params = [ param.replace(' ', '+') for param in filter(None, params) ]

        return ' '.join(params)

    def get_logquery(self):
        if not self.operators.search(self.params['what']):
            return self.params['what']
        return ''

    def get_geoquery(self):
        params = self.operators.split(self.params['where'])
        cities = settings.APP_GEO_CITIES.keys()

        geo = []

        for param in params:
            if param in cities:
                geo.append(settings.APP_GEO_CITIES[param])

        return geo

    def _clean_query(self, query, only_or=False):
        params = self.normalize.sub(' ', query).strip()
        params = self.operators_included.split(params)
        params = [ param.strip() if param else '' for param in params ]
        params = filter(None, params)

        if only_or:
            params = ['OR' if param == 'AND' else param for param in params ]

        query = []

        for i in xrange(0,len(params),2):
            if len(self.special_chars.sub('', params[i])) >= settings.SEARCH_MIN_QUERY_LENGTH:
                if i-1 > 0 and len(params) >= i-1: query.append(params[i-1].upper())
                query.append(params[i].lower())

        return ' '.join(query)

class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def timesince(dt, default=_(u'danes')):
    date = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    diff = now - date

    periods = (
        (diff.days / 365, _(u'letom'),   _(u'leti"')),
        (diff.days / 30,  _(u'mesecom'), _(u'meseci')),
        (diff.days / 7,   _(u'tednom'),  _(u'tedni')),
        (diff.days,       _(u'dnevom'),  _(u'dnevi')),
    )

    for period, singular, plural in periods:
        if period:
            return _(u'pred %d %s') % (period, singular if period == 1 else plural)

    return default
