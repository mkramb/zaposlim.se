from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.defaults import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('website',),
}

urlpatterns = patterns('',
    url(r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^locale/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^api/', include('website.apps.api.urls')),
    url(r'^', include('website.apps.common.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'website.urls.error_404'
handler500 = 'website.urls.error_500'

def error_404(request):
    return direct_to_template(request, '404.html')

def error_500(request):
    return direct_to_template(request, '500.html')
