import threading
import time
from datetime import timedelta
from django.utils import timezone
from django.db import close_old_connections
from django.db.models import F, ExpressionWrapper, DateTimeField

from .models import Answers_Everyweek_Tasks, Options
from .Utils.send_telegram_message import send_telegram_message


def notify_worker():
    """
    Фоновый поток: проверяет просроченные задания и отправляет уведомления.
    """
    while True:
        try:
            now = timezone.localtime()
            # print(f'now {now}')

            delta8days = now - timedelta(days=7)

            unfinished_everyweek_tasks = Answers_Everyweek_Tasks.objects.filter(
                Stars=None,
                NotificationSent=False,
                Date_Record__lt=delta8days
            )

            # print(f'unfinished_everyweek_tasks {unfinished_everyweek_tasks}')

            for task in unfinished_everyweek_tasks:
                deadline = task.Date_Record + timedelta(days=7)
                if now > deadline:
                    notify_time = task.TestID.People_ID.options.Notification_Week_Time
                    if notify_time and now.hour == notify_time.hour and now.minute == notify_time.minute:
                        rows_updated = Answers_Everyweek_Tasks.objects.filter(
                            id=task.id,
                            NotificationSent=False
                        ).update(NotificationSent=True)
                        print(f'rows_updated {rows_updated}')
                        if rows_updated:
                            # send_telegram_message(task.TestID.People_ID, f"Задание '{task.TaskID}' просрочено!")
                            send_telegram_message(task.TestID.People_ID.TG_ID, f"Задание '{task.TaskID.Name}' просрочено!")

        except Exception as e:
            print(f"[NotifyWorker ERROR]: {e}")
        finally:
            # Освобождаем соединения к БД
            close_old_connections()

        time.sleep(30)


def start_notify_worker():
    """
    Запускает поток в фоне (один раз при старте Django).
    """
    t = threading.Thread(target=notify_worker, daemon=True)
    t.start()
    print('Поток запущен')
