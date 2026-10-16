# Tasks API

Мини-бэкенд на FastAPI для управления задачами и категориями. Данные хранятся в PostgreSQL через SQLAlchemy 2.0, схемы валидируются Pydantic v2.

Установка: создай виртуальное окружение 
`python -m venv .venv`, 
активируй его и поставь зависимости 
`pip install fastapi "uvicorn[standard]" sqlalchemy "psycopg[binary]"`. 
Строка подключения к БД задаётся в переменной `DATABASE_URL` в начале `main.py`, таблицы создаются автоматически при старте приложения через `lifespan`.

Запуск: `uvicorn main:app --reload`. Документация Swagger доступна на http://127.0.0.1:8000/docs, ReDoc — на /redoc.

Эндпоинты задач: `GET /tasks` возвращает список всех задач, `POST /tasks` создаёт новую (201), `PATCH /tasks/{task_id}` частично обновляет поля `title` и `completed`, `DELETE /tasks/{task_id}` удаляет задачу (204). Пример создания: `curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Купить молоко"}'`. Модель задачи — `{"id": "uuid", "title": "string", "completed": false}`.

Эндпоинты категорий: `GET /categories`, `POST /categories` (201), `PATCH /categories/{category_id}`, `DELETE /categories/{category_id}` (204). Важно: категории сейчас хранятся в памяти процесса в списке `categories`, при перезапуске данные теряются, а модель `CategoryORM` объявлена, но не используется.

CORS разрешён только для `http://localhost:3000` — это настраивается в `CORSMiddleware`.

нет миграций (Alembic не подключён, схема создаётся через `Base.metadata.create_all`), нет пагинации в `GET /tasks`, нет аутентификации, категории не персистентны и не связаны с задачами