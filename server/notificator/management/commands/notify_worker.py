from django.core.management.base import BaseCommand
from notificator.notifications import notify_worker


class Command(BaseCommand):
    help = "Запускает воркер уведомлений"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Старт воркера уведомлений..."))
        notify_worker()