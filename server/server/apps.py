from django.apps import AppConfig
from django.conf import settings

from .config_loader import Config


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'
    verbose_name = "Проект \"Выгорание\""

    def ready(self):
        Config.load()
