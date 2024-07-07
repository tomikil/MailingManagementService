from django.core.management import BaseCommand

from mailings.services import start


class Command(BaseCommand):

    def handle(self, *args, **options):
        start()
