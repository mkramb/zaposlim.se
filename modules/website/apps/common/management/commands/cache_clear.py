from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear all cache.'

    def handle(self, *args, **kwargs):
        cache.clear()
        self.stdout.write("Successfully cleared all cache.\n")
