# -*- coding: utf-8 -*-

from django.conf import settings

from celery.task import Task
from celery.registry import tasks

import httplib, urllib

class RunSpiders(Task):
    def run(self):
        # run all spiders at once
        connection = httplib.HTTPConnection('localhost', 6800)
        headers = { 'Content-type': 'application/x-www-form-urlencoded' }
        logger = RunSpiders.get_logger()

        for index in settings.SEARCH_ALIASES:
            connection.request(
                'POST', '/schedule.json',
                urllib.urlencode({
                    'project' : 'scraper',
                    'spider'  : index,
                }), headers
            )

            logger.info(connection.getresponse().read())
        return True

tasks.register(RunSpiders)
