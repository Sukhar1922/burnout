from django.apps import AppConfig
from django.conf import settings

from .config_loader import Config


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = "Проект \"Выгорание\""

    def ready(self):
        import api.signals

        Config.load()

        # Запускаем фонового воркера только когда реально стартует сервер,
        # а не во время миграций/менеджмент-команд
        if settings.TG_BOT_ENABLE:
            import sys
            if "runserver" in sys.argv or "gunicorn" in sys.argv:
                from .notifications import start_notify_worker
                from .notificationsGen import start_generator_worker
                import os

                if os.environ.get("RUN_MAIN") == "true":
                    start_notify_worker()
                    # start_generator_worker()

                    pass
