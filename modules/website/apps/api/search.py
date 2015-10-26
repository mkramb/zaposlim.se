# -*- coding: utf-8 -*-

from website.apps.search.gateway import ElasticSearch

from piston.handler import BaseHandler
from piston.utils import rc

from django.db import connection

import logging
import re

logger = logging.getLogger('website.apps.api.search')
normalize_spaces = re.compile(' +')

class SearchHandler(BaseHandler):
    allowed_methods = ('POST',)

    def create(self, request):
        if not request.data.has_key('query'):
            return rc.BAD_REQUEST

        try:
            model = ElasticSearch(request.data.get('query'))
            model.search()

            data = {
                'query': model.query.params,
                'facets': model.get_facets(),
                'results': {
                    'items': model.get_results(),
                    'pagination': model.list_pages(),
                    'total': model.results.total
                }
            }

            if not len(data['results']['items']):
                data['results'] = []

            if model.results.total > 0 and len(model.query.params['what']):
                what = model.query.get_logquery()

                if len(what) and model.query.params['page'] == 1:
                    if not model.query.params.has_key('company.facet') and model.query.params['sorting'] == '_score':
                        cursor = connection.cursor()
                        cursor.execute(
                           "INSERT DELAYED INTO search_log (what, updated_date) VALUES (%s, NOW()) " \
                           "ON DUPLICATE KEY UPDATE count = count + 1, updated_date = NOW()",
                           [what]
                        )

            model.close()
            return data

        except Exception, err:
            logger.exception('ERROR: %s\n' % unicode(err))

            return {
                'query': request.data.get('query'),
                'results': []
            }
