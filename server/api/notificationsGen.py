import threading
import time
from datetime import timedelta

from django.db import close_old_connections
from django.utils import timezone

from .models import Answers_Everyweek_Tasks, NotificationEvent


def generate_unfinished_task_notifications(now_attr):
    now = now_attr
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=31)
    print(f'week ago: {week_ago}')
    print(f'month ago: {month_ago}')

    unfinished_tasks = Answers_Everyweek_Tasks.objects.filter(
        Stars__isnull=True,
        Date_Record__range=(month_ago, week_ago)
        # Date_Record__gte=month_ago,
        # Date_Record__lte=week_ago,
    ).select_related("TestID__People_ID", "TaskID", "TestID__People_ID__options")
    print(f'unfinished_tasks: {unfinished_tasks}')

    for task in unfinished_tasks:
        person = task.TestID.People_ID
        options = getattr(person, "options", None)

        if not options or not options.Notification_Week or not options.Notification_Week_Time:
            continue  # уведомления отключены или нет времени

        # Проверяем, нет ли уже активного уведомления на это задание
        if NotificationEvent.objects.filter(
                People_ID=person,
                Message__icontains=task.TaskID.Name,
                Sent=False
        ).exists():
            continue

        # Время из настроек
        scheduled_time = timezone.make_aware(
            timezone.datetime.combine(now.date(), options.Notification_Week_Time)
        )

        # Если время уже прошло сегодня — переносим на завтра
        if scheduled_time <= now:
            scheduled_time += timedelta(days=1)

        NotificationEvent.objects.create(
            People_ID=person,
            Message=f"Задание \'{task.TaskID.Name}\' просрочено",
            Scheduled_at=scheduled_time
        )
        print('Создано уведомление')


def generator_worker():
    GENERATOR_SLEEP = 30

    while True:
        print('Итерация генератора')
        try:
            now = timezone.localtime()

            # Прошла неделя, но пользователь не оценил задание
            generate_unfinished_task_notifications(now)

        except Exception as e:
            print(f"[GeneratorWorker ERROR]: {e}")
        finally:
            close_old_connections()
        time.sleep(GENERATOR_SLEEP)

def start_generator_worker():
    """
    Запускает поток в фоне (один раз при старте Django).
    """
    t = threading.Thread(target=generator_worker, daemon=True)
    t.start()
    print('Поток генератора запущен')
