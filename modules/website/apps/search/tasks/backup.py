# -*- coding: utf-8 -*-

from website.apps.common.models import DataBackup
from django.conf import settings

from celery.task import Task
from celery.registry import tasks

import os

class BackupData(Task):
    def run(self):
        logger = BackupData.get_logger()

        # backup past day scraping to filesystem
        for backup in DataBackup.objects.order_by('-created_date'):
            folder = os.path.join(settings.BACKUP_INDICES, backup.created_date.strftime('%Y_%m'))

            if not os.path.exists(folder):
                os.makedirs(folder)

            file = open(
                os.path.join(folder, '%s_%s' %
                    (backup.created_date.strftime('%d'), backup.name)
                ), 'w'
            )

            file.write(backup.source)
            file.close()

            backup.delete()
            logger.info('Created backup for spider:%s, date:%s' %
                (backup.name, backup.created_date.strftime('%Y.%m.%d'))
            )

        return True

tasks.register(BackupData)
