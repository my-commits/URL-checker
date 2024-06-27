# URL Checker

## Запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   cd url_checker
2. Запустите Docker:
    ```bash
    docker-compose up --build
3. Выполните миграции:
    ```bash
    docker-compose run web python manage.py migrate
4. Создайте суперпользователя:
    ```bash
    docker-compose run web python manage.py createsuperuser

## API
- Регистрация: POST /auth/users/
- Логин: POST /auth/token/login/
- CRUD для URL:
- GET /api/urls/
- POST /api/urls/
- GET /api/urls/<id>/
- PUT /api/urls/<id>/
- DELETE /api/urls/<id>/
- Bulk методы:
  - POST /api/urls/bulk_create/
  - PUT /api/urls/bulk_update/

## Периодическая проверка URL
- Команда для ручного запуска проверки:
    ```bash
    docker-compose run web python manage.py check_urls
