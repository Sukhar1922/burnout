### Требования
- git
- python 3.12 (тестировалось на python 3.12.10)
- PostgreSQL (тестировалось на 17.5)

### Установка 
    1. python -m venv venv
    2. Для Win:
        venv/scripts/activate
    2. Для Linux:
        source venv/bin/activate
    3. pip install -r requirements.txt
    4. cd server
    5. cp .env.example .env
    6. Установить свою конфигурацию для бд на postgreSQL с помощью vim .env

### Запуск
    1. Для Win:
        venv/scripts/activate
    1. Для Linux:
        source venv/bin/activate
    2. cd server
    3. Для Win:
        python manage.py runserver 0.0.0.0:80
    3. Для Linux:
        python3.12 manage.py runserver 0.0.0.0:80
Если запускать на локальной машине, то ip адрес и порт указывать не нужно

### Админка
- Адрес - http://kgu.red-atom.ru/admin
- Логин - admin
- Пароль - admin

### Интересные адреса на сервере
- https://kgu.red-atom.ru/api/
- https://kgu.red-atom.ru/admin/

### API
    GET:
        api/questions_368c231b7c9a3d506cef5a936c83d92f068179d849db19ac2608ba288c7c1c56:
            Нет параметров.
            Возвращает все вопросы (id, название)
        api/fill_table_808b0abd590b48de048dfef7abadcd06410a24c9f9619a05aef83a9eb30ad765:
            Нет параметров.
            Служеюное API для заполнения таблицы вопросов, если внутри функции fillQuestions flag = True
            Возвращает результат обновления (Удачно, неудачно, нет разрешения)
