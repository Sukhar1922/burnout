Для полной установки django нужно выполнить:
    1. python -m venv venv
    2. Для Win:
        venv/scripts/activate
    2. Для Linux:
        source venv/bin/activate
    3. pip install -r requirements.txt

Для запуска django проекта:
    1. Для Win:
        venv/scripts/activate
    1. Для Linux:
        source venv/bin/activate
    2. cd server
    3. Для Win:
        python manage.py runserver
    3. Для Linux:
        python3.12 manage.py runserver

Вероятно, чтобы работало из вне, после runserver указать 0.0.0.0:80
Это временное решение

Админка:
Адрес - http://адрес:порт/admin
Логин - admin
Пароль - admin

API:
    GET:
        api/questions_368c231b7c9a3d506cef5a936c83d92f068179d849db19ac2608ba288c7c1c56:
            Нет параметров.
            Возвращает все вопросы (id, название)
