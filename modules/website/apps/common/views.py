# -*- coding: utf-8 -*-

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.cache import never_cache
from django.conf import settings

from models import count_documents

from pyes import ES
from pyes.exceptions import NotFoundException

def home(request):
    return direct_to_template(request, 'base.html',
        {'job_count': count_documents()}
    )

@never_cache
def job_redirect(request, slug, source, job_id):
    if request.method == 'GET' and request.GET.has_key('redirect'):
        try:
            elastic = ES(settings.SEARCH_HOSTS)
            data = elastic.get(source, 'job', job_id)
            elastic.connection.close()
            return HttpResponseRedirect(data['_source']['details_url'])
        except NotFoundException:
            raise Http404

    return direct_to_template(request, 'pages/redirect.html')
