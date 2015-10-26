# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('website.apps.common.views',
    url(r'^oglas/(?P<slug>.+)/(?P<source>.+)/(?P<job_id>.*)/$', 'job_redirect', name='redirect'),
    url(r'^$', 'home', name='home'),
)
