import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../lib')

os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)

# UNCOMMENT TO ENABLE MONITORING
#import wsgi.wsgi_monitor as monitor
#monitor.start(interval=1.0)
