from django.http import HttpResponseNotFound
from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from django.template.loaders.filesystem import Loader
from django.template import RequestContext
from django.test.client import RequestFactory

from website.apps.common.models import count_documents
from website.apps.api.comon import StatsHandler
from website.apps.api.search import SearchHandler

from utils import rewrite_params, InjectRequest
from piston.utils import rc

import pystache
import urllib2

def home(request):
    geo = StatsHandler().read({}, 'geo')
    stats = StatsHandler().read({}, 'queries')
    template = Loader().load_template_source('pages/home/stats.html')[0]

    content = render_to_string('pages/home.html', {
        'job_top': pystache.render(template, {'queries': stats['top']}),
        'job_latest': pystache.render(template, {'queries': stats['latest']}),
        'job_cities':  [ city[1] for city in geo ]
    }, context_instance=RequestContext(request))

    return direct_to_template(request, 'base.html', {
         'home': content, 'job_count': count_documents()
    })

def stats(request):
    params = rewrite_params(request)
    title = None

    if params.has_key('popularna-iskanja'):
        title = 'Popularna iskanja'
        query = 'top'
    elif params.has_key('zadnja-iskanja'):
        title = 'Zadnja iskanja'
        query = 'latest'
    else:
        return rc.BAD_REQUEST

    fake_request = RequestFactory().get('?query=%s' % query)
    stats = StatsHandler().read(fake_request, 'searches')
    template = Loader().load_template_source('pages/stats/items.html')[0]

    content = render_to_string('pages/stats.html', {
        'title': title,
        'stats': pystache.render(template, stats)
    }, context_instance=RequestContext(request))

    return direct_to_template(request, 'base.html', {
         'search': content
    })

def results(request):
    params = rewrite_params(request).copy()
    del params['_escaped_fragment_']

    if not len(params):
        return HttpResponseNotFound()

    if not params.has_key('page'): params['page'] = 1
    if not params.has_key('sorting'): params['sorting'] = '_score'

    query = {}

    for param in params:
        query[param] = urllib2.unquote(unicode(params[param]))

    search = SearchHandler().create(InjectRequest(query))
    loader = Loader()

    items = pystache.render(
        loader.load_template_source('pages/search/items.html')[0],
        search['results']
    )

    facets = ''

    if search.has_key('facets') and search['facets'].has_key('company.facet'):
        facets = pystache.render(
            loader.load_template_source('pages/search/facets.html')[0],
            {'facets' : search['facets']['company.facet']}
        )

    term = ''

    if (query.has_key('what') and len(query['what'])) and (query.has_key('where') and len(query['where'])):
        term = '%s / %s' % (query['what'].lower(), query['where'].lower())
    elif query.has_key('what'): term = query['what'].lower()
    elif query.has_key('where'): term = query['where'].lower()

    total = 0

    if len(search['results']):
        total = search['results']['total']

    pagination = ''

    if len(search['results']) and len(search['results']['pagination']) > 1:
        pagination =  pystache.render(
            loader.load_template_source('pages/search/pagination.html')[0],
            {'pagination' : search['results']['pagination'] }
        )

    content = render_to_string('pages/search.html', {
        'term': term, 'total': total, 'facets': facets,
        'items': items, 'pagination': pagination
    }, context_instance=RequestContext(request))

    return direct_to_template(request, 'base.html', {
         'search': content, 'job_count': count_documents()
    })
