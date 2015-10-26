# -*- coding: utf-8 -*-

import httplib, urllib
import os

# init django enviroment
from scraper.utils import setup_django_env
from django.conf import settings

BIN_ROOT = os.path.abspath(os.path.dirname(__file__))
setup_django_env(os.path.join(BIN_ROOT, '../modules/website/'))

connection = httplib.HTTPConnection('localhost', 6800)
headers = { 'Content-type': 'application/x-www-form-urlencoded' }

for index in settings.SEARCH_ALIASES:
    connection.request(
        'POST', '/schedule.json',
        urllib.urlencode({
            'project' : 'scraper',
            'spider'  : index,
        }), headers
    )
            
    print connection.getresponse().read()
