# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from website.apps.common.fields import JSONField
from website.apps.search.templatetags.template_additions import truncate

class LogManager(models.Manager):
    def top_items(self, limit = settings.APP_SEARCHES_TOP):
        return self.order_by('-count')[:limit]

    def last_items(self, limit = settings.APP_SEARCHES_LAST):
        return self.order_by('-updated_date')[:limit]

class Log(models.Model):
    what = models.CharField(max_length=120, unique=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)
    count = models.PositiveIntegerField(default=1)
    objects = LogManager()

    @property
    def what_short(self):
        return truncate(self.what, settings.APP_SEARCHES_LENGTH)

class City(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    indices = JSONField()
