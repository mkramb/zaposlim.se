# -*- coding: utf-8 -*-

from comon import AutocompleteHandler, StatsHandler, PagesHandler, ContactHandler
from search import SearchHandler

from django.conf.urls.defaults import patterns, url
from piston.resource import Resource

urlpatterns = patterns('website.api.views',
    url(r'^search/$', Resource(SearchHandler)),
    url(r'^autocomplete/(?P<param>\w+)/$', Resource(AutocompleteHandler)),
    url(r'^stats/(?P<param>\w+)/$', Resource(StatsHandler)),
    url(r'^pages/$', Resource(PagesHandler)),
    url(r'^pages/contact/$', Resource(ContactHandler)),
) 
