from django.db import models
from django.template.defaultfilters import slugify
from django.core.cache import cache
from django.conf import settings

from website.apps.common.fields import JSONField
from pyes import ES

class Data(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    source = JSONField()

class DataBackup(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    created_date = models.DateField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True)
    source = models.TextField()
    
    class Meta:
        unique_together = ('name', 'created_date')

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    content = models.TextField()

    def save(self):
        if not self.id:
            self.slug = slugify(self.title)

        super(Page, self).save()

class CrawlerLog(models.Model):
    url = models.CharField(max_length=512)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.TextField()
    content_length = models.IntegerField()
    client_ip = models.CharField(max_length=512)
    client_useragent = models.CharField(max_length=512)
    request = JSONField()

def count_documents():
    num_docs = cache.get('website.documents_count')

    if not num_docs:
        elastic = ES(settings.SEARCH_HOSTS)
        indices = elastic.get_indices()
        elastic.connection.close()

        indices = indices.values()
        num_docs = 0

        for item in indices:
            num_docs += item['num_docs']

        cache.set('website.documents_count', num_docs)

    return num_docs
