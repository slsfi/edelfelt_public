from django.core.management.base import BaseCommand
from django.core.cache import *
class Command(BaseCommand):
    args = 'no args'
    help = 'Clears the cache (cache.clear())'
    def handle(self, *args, **options):
        cache.clear()