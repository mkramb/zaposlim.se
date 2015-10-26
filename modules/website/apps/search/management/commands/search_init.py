from django.core.management.base import BaseCommand
from django.conf import settings

from website.apps.search.mapping import mapping
from pyes import ES

from optparse import make_option
import time

class Command(BaseCommand):
    args = '<alias_name alias_name ...>'
    help = 'Create indices mapping.'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true', dest='all', default=False,
            help='Create indices mapping.'),
    )

    def handle(self, *args, **kwargs):
        init_all = kwargs.get('all')

        elastic = ES(settings.SEARCH_HOSTS)
        aliases = settings.SEARCH_ALIASES if init_all else args
        indices_new = []

        for alias in aliases:
            index_new = '%s_%d' % (alias, int(time.time()))
            indices_new.append(index_new)

            elastic.create_index_if_missing(index_new)
            elastic.add_alias(alias, [index_new])

        if len(aliases):
            elastic.put_mapping('job', {'job':{'properties':mapping}}, indices_new)
            self.stdout.write("Successfully created indices mapping.\n")

        elastic.connection.close()
