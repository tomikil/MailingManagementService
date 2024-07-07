from django.apps import AppConfig
from time import sleep


class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'

    def ready(self):
        from mailings.services import start
        sleep(5)
        start()

