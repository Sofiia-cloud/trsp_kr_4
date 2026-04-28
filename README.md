
## УСТАНОВКА И ЗАПУСК

1. Клонирование репозитория

   git clone <your-repo-url>

2. Создание виртуального окружения

   python -m venv venv
   venv\Scripts\activate

3. Установка зависимостей

   pip install -r requirements.txt

4. Настройка переменных окружения

   cp .env.example .env

5. Применение миграций Alembic

   alembic upgrade head

6. Запуск приложения

   uvicorn app.main:app --reload

   Приложение будет доступно:
   - http://localhost:8000
   - Документация API: http://localhost:8000/docs

---

## ТЕСТИРОВАНИЕ

Запуск всех тестов:

pytest -v

Запуск конкретного набора тестов:

pytest tests/test_errors.py -v
pytest tests/test_validation.py -v
pytest tests/test_users_async.py -v

---

## ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ (примеры запросов)

1. Проверка пользовательских исключений (задание 10.1)

   Вызов CustomExceptionA (400 - Bad Request):
   curl "http://localhost:8000/trigger-a?value=-5"

   Вызов CustomExceptionB (404 - Not Found):
   curl "http://localhost:8000/trigger-b/0"

   Нормальные запросы:
   curl "http://localhost:8000/trigger-a?value=10"
   curl "http://localhost:8000/trigger-b/42"

2. Проверка валидации (задание 10.2)

   Успешная регистрация:
   curl -X POST "http://localhost:8000/register" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"john\",\"age\":25,\"email\":\"john@test.com\",\"password\":\"secure123\"}"

   Ошибка валидации (возраст 18 или меньше):
   curl -X POST "http://localhost:8000/register" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"john\",\"age\":18,\"email\":\"john@test.com\",\"password\":\"secure123\"}"

3. Проверка CRUD пользователей (задание 11.2)

   Создание пользователя:
   curl -X POST "http://localhost:8000/users" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"alice\",\"age\":30}"

   Получение пользователя (подставьте ID из ответа создания):
   curl "http://localhost:8000/users/1"

   Удаление пользователя:
   curl -X DELETE "http://localhost:8000/users/1"

