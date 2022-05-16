# KefirTestApi

Проект KefirTestApi - это REST сервис для хранения и предоставления данных о пользователях.
### Функционал
- Аутентификация в сервисе происходит с помощью cookie.
- Администраторы могут видеть все данные пользователей и изменять их.
- Простые пользователи могут видеть лишь ограниченное число данных обо всех пользователях и редактировать часть своих данных.
- Добавлять и редактировать данные о пользователе можно через админку.

### Интересное
- Кастомная модель пользователя.
- В качестве логина используется email.
- Аутентификация пользователя с помощью cookie.
- Для каждого метода написаны тесты.
- SWAGGER.

**Ссылки**:
- [Telegram](https://t.me/teslo_a)

### Инструменты

- Python >= 3.9
- Django Rest Framework
- Docker
- Postgres
- NGINX

## Старт

#### 1) Переименовать "api\api\.env copy" на "api\api\.env" и прописать свои настройки

    SECRET_KEY=django_key
    ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    
    POSTGRES_DB=имя_твоей_бд
    POSTGRES_ENGINE=django.db.backends.postgresql
    POSTGRES_USER=имя_твоего_пользователя
    POSTGRES_PASSWORD=пароль_бд
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    

#### 2) Создать образ и запустить контейнер

    docker-compose up --build

##### 3) Создать супер юзера

    docker exec -it kefir_api_web bash
    python manage.py createsuperuser

##### 3.1) В случае необходимости можно запустить тесты
    python manage.py test

##### 4) Перейти по адресу

    http://localhost/swagger/

##### 4.1) Для доступа к админке перейти по адресу

    http://localhost/admin/

 
 ##### 0) Если нужно очистить БД

    docker-compose down -v
 
## License

[BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

Copyright (c) 2022-present, alteslo - Teslenko Alexander