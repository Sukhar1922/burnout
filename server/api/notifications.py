import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()


import threading
import time
from datetime import timedelta

from django.utils import timezone
from django.db import close_old_connections
from django.db.models import F, ExpressionWrapper, DateTimeField
from django.contrib.contenttypes.models import ContentType

from api.config_loader import Config
from .models import Answers_Everyweek_Tasks, Options, NotificationEvent, Test_Burnout
from .Utils.send_telegram_message import send_telegram_message


class Notification:
    """
    Класс для удобного хранения полей для создания таблицы NotificationEvent.
    """
    def __init__(self, People_ID, Message, content_type, object_id):
        self.people_id = People_ID
        self.message = Message
        self.content_type = content_type
        self.object_id = object_id


def unfinished_task_notifications(now_attr):
    """
    Генератор уведомлений для ситуации, когда с момента взятия задания прошло более 7 дней.
    Уведомляет пользователя, что пора бы оценить задание.
    Берёт все незавершённые задания, проверят, что пользователь не получал уведомление, и возвращает список уведомлений.
    :param now_attr: Параметр для передачи времени начала итерации воркера.
    :return: Список с уведомлениями.
    """
    now = now_attr
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=31)

    notifications = []

    unfinished_tasks = Answers_Everyweek_Tasks.objects.filter(
        Stars__isnull=True,
        Date_Record__range=(month_ago, week_ago)
    ).select_related("TestID__People_ID", "TaskID", "TestID__People_ID__options")

    task_ct = ContentType.objects.get_for_model(Answers_Everyweek_Tasks)

    existing = set(
        NotificationEvent.objects.filter(
            content_type=task_ct,
            object_id__in=[t.id for t in unfinished_tasks]
        ).values_list("object_id", flat=True)
    )

    for task in unfinished_tasks:
        person = task.TestID.People_ID
        options = getattr(person, "options", None)

        if not options or not options.Notification_Week:
            continue  # уведомления отключены

        # Проверяем, есть ли уже уведомление для этого задания и пользователя
        if task.id in existing: continue

        message = Config.config['notifications']['unfinished_task'].format(task_name=task.TaskID.Name)
        notifications.append(Notification(person, message, task_ct, task.id))

    return notifications


def uncompleted_test_notification(now_attr):
    """
    Генератор уведомлений для ситуации, когда пользователь не прошёл ежемесячный тест.
    Уведомляет пользователя, что нужно пройти тест.
    Берёт последние тесты, которые были месяц назад. Проверят, что на последнем тесте есть оценка, проверят включённость
    уведомлений у пользователя, после чего добавляет уведомления.
    :param now_attr: Параметр для передачи времени начала итерации воркера.
    :return: Список с уведомлениями.
    """
    now = now_attr
    month_ago = now - timedelta(days=31)
    three_month_ago = now - timedelta(days=31*3)

    notifications = []

    # Берём последние тесты для каждого пользователя
    last_tests = (
        Test_Burnout.objects.filter(Date_Record__range=(three_month_ago, month_ago))
        .select_related("People_ID")
        .order_by("People_ID", "-Date_Record")
    )

    test_ct = ContentType.objects.get_for_model(Test_Burnout)
    message = Config.config['notifications']['uncompleted_test']

    existing = set(
        NotificationEvent.objects.filter(
            content_type=test_ct,
            object_id__in=[t.id for t in last_tests],
            Message=message,
        ).values_list("object_id", flat=True)
    )

    # Чтобы не брать старые тесты одного и того же человека
    seen_people = set()
    for test in last_tests:
        person = test.People_ID
        options = getattr(person, "options", None)

        if not options or not options.Notification_Week:
            continue  # уведомления отключены

        if test.People_ID_id in seen_people:
            continue
        seen_people.add(test.People_ID_id)

        # Проверяем, что все задания по тесту оценены
        has_unfinished = Answers_Everyweek_Tasks.objects.filter(
            TestID=test, Stars__isnull=True
        ).exists()
        if has_unfinished:
            continue

        if test.id in existing: continue

        # Добавляем уведомление в список
        notifications.append(
            Notification(
                People_ID=test.People_ID,
                Message=message,
                content_type=test_ct,
                object_id=test.id,
            )
        )

    return notifications


def unselected_task_notification(now_attr):
    """
    Генератор уведомлений, на случай, если пользователь день назад прошёл тест, но не взял задание.
    Уведомляет пользователя, что надо взять еженедельное задание.
    Берёт последние тесты, проверят, что для них нет активных заданий, у пользователя включены уведомления.
    :param now_attr: Параметр для передачи времени начала итерации воркера.
    :return: Список с уведомлениями.
    """
    now = now_attr
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)

    notifications = []

    last_tests = (
        Test_Burnout.objects.filter(Date_Record__range=(week_ago, day_ago))
        .select_related("People_ID")
        .order_by("People_ID", "-Date_Record")
    )

    test_ct = ContentType.objects.get_for_model(Test_Burnout)
    message = Config.config['notifications']['unselected_task']

    existing = set(
        NotificationEvent.objects.filter(
            content_type=test_ct,
            object_id__in=[t.id for t in last_tests],
            Message=message,
        ).values_list("object_id", flat=True)
    )

    seen_people = set()
    for test in last_tests:
        person = test.People_ID
        options = getattr(person, "options", None)

        if not options or not options.Notification_Week:
            continue  # уведомления отключены

        if test.People_ID_id in seen_people:
            continue
        seen_people.add(test.People_ID_id)

        # Проверяем, что все задания по тесту оценены
        has_tasks = Answers_Everyweek_Tasks.objects.filter(
            TestID=test
        ).exists()
        if has_tasks:
            continue

        if test.id in existing: continue

        # Добавляем уведомление в список
        notifications.append(
            Notification(
                People_ID=test.People_ID,
                Message=message,
                content_type=test_ct,
                object_id=test.id,
            )
        )

    return notifications


def notify_worker():
    """
    Воркер уведомлений, который запускается параллельно основному приложению Django.
    Раз в заданное время проверя, нужно ли отправлять уведомления. Отправленные уведомления сохраняются в бд.

    :return:
    """
    NOTIFICATION_SLEEP = Config.config["timers"]["notification_sleep"]
    # print(NOTIFICATION_SLEEP)
    while True:
        try:
            # print('Итерация уведомлений')
            now = timezone.localtime()
            print(f'[{now}] Итерация')
            event_groups = []

            # Здесь указываются функции, которые собирают уведомления
            event_groups.append(unfinished_task_notifications(now))
            event_groups.append(uncompleted_test_notification(now))
            event_groups.append(unselected_task_notification(now))

        except Exception as e:
            print(f"[NotifyWorker generator ERROR]: {e}")

        try:
            all_events_to_save = []

            try:
                for event_group in event_groups:
                    for event in event_group:
                        # пробуем отправить сообщение
                        send_telegram_message(event.people_id.TG_ID, event.message)

                        # если не упало → готовим объект к записи
                        all_events_to_save.append(NotificationEvent(
                            People_ID=event.people_id,
                            Message=event.message,
                            content_type=event.content_type,
                            object_id=event.object_id
                        ))

            except Exception as send_err:
                print(f"[NotifyWorker send ERROR]: {send_err}")

            # если хоть что-то удалось отправить → сохраняем пачкой
            if all_events_to_save:
                NotificationEvent.objects.bulk_create(all_events_to_save)

        except Exception as e:
            print(f"[NotifyWorker worker ERROR]: {e}")
        finally:
            close_old_connections()
        time.sleep(NOTIFICATION_SLEEP)


def start_notify_worker():
    """
    Запускает поток в фоне (один раз при старте Django).
    """
    # NOTIFICATION_SLEEP = Config.config["timers"]["notification_sleep"]
    # print(NOTIFICATION_SLEEP)
    t = threading.Thread(target=notify_worker, daemon=True)
    t.start()
    print('Поток запущен')


# if __name__ == '__main__':
#
#     notify_worker()
