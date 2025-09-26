import threading
import time
from datetime import timedelta
from django.utils import timezone
from django.db import close_old_connections
from django.db.models import F, ExpressionWrapper, DateTimeField

from .models import Answers_Everyweek_Tasks, Options, NotificationEvent
from .Utils.send_telegram_message import send_telegram_message


def notify_worker():
    while True:
        try:
            print('Итерация уведомлений')
            now = timezone.localtime()
            events = NotificationEvent.objects.filter(
                Sent=False,
                Scheduled_at__lte=now
            )

            for event in events:
                if event.People_ID.options.Notification_Week:
                    # а ещё проверять, что пользовательн е выключил уведомления
                    send_telegram_message(event.People_ID.TG_ID, event.Message)
                    event.Sent = True
                    event.Sent_at = now
                    event.save(update_fields=["Sent", "Sent_at"])
                else:
                    event.Sent = True
                    event.save(update_fields=["Sent"])

        except Exception as e:
            print(f"[NotifyWorker ERROR]: {e}")
        finally:
            close_old_connections()
        time.sleep(30)


def start_notify_worker():
    """
    Запускает поток в фоне (один раз при старте Django).
    """
    t = threading.Thread(target=notify_worker, daemon=True)
    t.start()
    print('Поток запущен')
