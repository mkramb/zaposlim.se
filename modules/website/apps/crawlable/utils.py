from django.http import QueryDict

class InjectRequest(object):
    def __init__(self, query):
        self.data = {'query': query}

def rewrite_params(request):
    params = request.GET.copy()
    url = ''

    if request.GET.get('_escaped_fragment_', None):
        for key, value in params.items():
            url += u'&%s=%s' % (key, value.replace('?', '&'))
            
    return QueryDict(url)
