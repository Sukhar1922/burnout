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
- Адрес - http://kgu.red-atom.ru/django/admin
- Логин - admin
- Пароль - admin

### Интересные адреса на сервере
- https://kgu.red-atom.ru/django/api/
- https://kgu.red-atom.ru/django/admin/

### API
    GET:
        api/questions_368c231b7c9a3d506cef5a936c83d92f068179d849db19ac2608ba288c7c1c56:
            Нет параметров.
            Возвращает все вопросы (id, название)
        api/statistics_26a73614cf8dd8f7aeffec47fef1b6201896ece31e52a0c706ad5b7513f7851a:
            Параметр: TG_ID
            Возвращает все результаты тестов [[{time:timestamp}, [результаты]], [...], ...]
        api/check_people_0bb97721ff2c77036c66e6953a6ea632a424e36e6730fe74df52e3bbe6fcfa66:
            Параметр: TG_ID
            Возвращает true или false в зависимоти от наличия в бд пользователя
        api/everyweek_tasks_4a73556cb2e8ca050437f3868dccef0cee3bb02b5beb1b8d46882a43e452522e:
            Параметр: TG_ID
            Возвращает список заданий для последнего выполненого теста пользователем,
            Отбирает задания по наибольшей фазе.
            Формат вывода {
                "tasks": [Список из словарей заданий], 
                "took_tasks": [Список из id взятых заданий от самого свежего]
            }
    POST:
        api/registration_8d6238094a7742ac22fedb3a180bc590d35f5ea70b8a262cc0bd976349b6181d:
            Параметры регистрации Name, Surname, Partonymic, Email, Birthday, TG_ID
            Служит для получения данных регистрации на сервер
            Возвращает echo-ответ (Для тестирования)
        api/answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619:
            Параметры для обработки ответов {TG_ID:строка, [{id:число, answer:число}, {...}, .., {id:число, answer:число}}
            Служит для получения ответов пользователя
            Возвращает 12 результатов и время выполнения (Для тестирования)
            В случае, если пользователя с TG_ID нет в базе, то результаты в бд не записываются
        api/everyweek_tasks_4a73556cb2e8ca050437f3868dccef0cee3bb02b5beb1b8d46882a43e452522e:
            Параметры для взятия задания TG_ID, TaskID,
            Служит для добавления задания к выполненому тесту
            В случае успешного добавления задания, возвращает сообщение с id созданного задания
    PATCH:
        api/everyweek_tasks_4a73556cb2e8ca050437f3868dccef0cee3bb02b5beb1b8d46882a43e452522e:
            Параметры для завершения задания TG_ID, Stars, Comments,
            Служит для заполнения последнего еженедельного задания
            Stars должно быть числом от 1 до 5, Comments можно оставить пустым
            Возвращает сообщение, что задача обновлена с указаным числом звёздочек
            