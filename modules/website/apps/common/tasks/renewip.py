# -*- coding: utf-8 -*-

from django.conf import settings

from celery.task import Task
from celery.registry import tasks

from TorCtl import TorCtl

class RenewIp(Task):
    def run(self):
        # force to TOR to allocate new IP
        conn = TorCtl.connect(passphrase=settings.TOR_PASSPHRASE)

        if conn.is_live():
            conn.sendAndRecv('signal newnym\r\n')
            
        conn.close()
        return True

tasks.register(RenewIp)
