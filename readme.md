### Требования
- git
- python 3.12 (тестировалось на python 3.12.10)

### Установка 
    1. python -m venv venv
    2. Для Win:
        venv/scripts/activate
    2. Для Linux:
        source venv/bin/activate
    3. pip install -r requirements.txt

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
