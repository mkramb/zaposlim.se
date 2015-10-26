from django.core.management.base import BaseCommand
from django.conf import settings

from pyes import ES
from optparse import make_option

class Command(BaseCommand):
    args = '<source_name source_name ...>'
    help = 'Delete specific source (indicies & aliases).'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true', dest='all', default=False,
            help='Delete all sources (indicies & aliases).'),
    )

    def handle(self, *args, **kwargs):
        delete_all = kwargs.get('all')
        elastic = ES(settings.SEARCH_HOSTS)
        indices = []

        if delete_all:
            indices.extend(elastic.get_indices(True))
            indices.extend(elastic.get_closed_indices())

            for index in indices:
                elastic.delete_index_if_exists(index)
        else:
            for source_name in args:
                indices_aliased = [index for index in elastic.get_alias(source_name) if index == source_name]
                elastic.delete_index_if_exists(source_name)

                if indices_aliased:
                    elastic.delete_alias(source_name, indices_aliased)

                    for index in indices_aliased:
                        elastic.delete_index_if_exists(index)

        if len(indices) and len(args):
            elastic.connection.close()
            self.stdout.write("Successfully deleted indicies & aliases.\n")

        elastic.connection.close()
