from django.core.management.base import BaseCommand
from django.conf import settings

from pyes import ES
from optparse import make_option

class Command(BaseCommand):
    help = 'List all aliases.'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true', dest='all', default=False,
            help='List all indicies & aliases.'),
    )

    def handle(self, *args, **kwargs):
        list_all = kwargs.get('all')

        elastic = ES(settings.SEARCH_HOSTS)
        indices = elastic.cluster_state()['metadata']['indices']
        listing = []
        
        for key in indices.keys():
            listing.extend([key])

            if list_all:
                listing.extend(indices[key]['aliases'])

        for item in sorted(listing):
            self.stdout.write(item + "\n")

        elastic.connection.close()
