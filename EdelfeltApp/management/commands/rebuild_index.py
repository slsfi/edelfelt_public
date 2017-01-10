from subprocess import call

from django.conf import settings
from haystack.management.commands.rebuild_index import Command as RebuildCommand
import os

class Command(RebuildCommand):
    """
    Extend rebuild_index command from haystack app. This takes precedence as
    EdelfeltApp is later in INSTALLED_APPS.

    This is basically a hack to set liberal permissions on index directory which is
    destroyed and recreated every time indexes are cleared or rebuilt.
    """

    def handle(self, **options):
        super(Command, self).handle(**options)
        if os.name != 'nt':
            print "Set whoosh_index permissions"
            whoosh_dir = settings.HAYSTACK_CONNECTIONS['default']['PATH']
            call(['chmod', '777', whoosh_dir])
