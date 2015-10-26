from django.core.management.base import BaseCommand
from django.conf import settings

from pyes import ES
import pprint

class Command(BaseCommand):
    help = 'List indicies info.'

    def handle(self, *args, **kwargs):
        elastic = ES(settings.SEARCH_HOSTS)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(elastic.get_indices())

        elastic.connection.close()
