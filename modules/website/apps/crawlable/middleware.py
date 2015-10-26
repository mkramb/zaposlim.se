from views import home, results, stats
from website.apps.common.models import CrawlerLog

class CrawlableMiddleware(object):
    handlers = {
        u'zaposlitev': lambda request: results(request),
        u'stats': lambda request: stats(request),
    }

    def process_view(self, request, view, args, kwargs):

        if not request.is_ajax() and request.method == 'GET':
            fragment = request.GET.get('_escaped_fragment_', None)

            if fragment or fragment == '':
                request.is_crawler = True
                response = None

                for key in self.handlers.keys():
                    if fragment.find(key) == 0:
                        response = self.handlers[key](request)
                        break

                if not response:
                    response = home(request)

                self._log_response(request, response)
                return response

    def _log_response(self, request, response):
        log = CrawlerLog()
        log.url = request.get_full_path()

        log.content = response.content
        log.content_length = len(response.content)

        log.client_useragent = request.META.get('HTTP_USER_AGENT')
        log.client_ip = self._get_client_ip(request)

        log.request = dict((header, value)
             for (header, value) in request.META.items()
                if header.startswith('HTTP_'))

        log.save()

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
