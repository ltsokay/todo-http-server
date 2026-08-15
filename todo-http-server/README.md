# TODO HTTP Server

REST API для управления задачами на Flask. Поддерживает создание, чтение, обновление и удаление задач, хранение состояния в файле, логирование и запуск в Docker.

## Возможности

- Создание, получение, обновление и удаление задач (CRUD)
- Отметка задачи выполненной
- Приоритет задачи (`priority`) и статус выполнения (`isDone`)
- Персистентное хранение — данные сохраняются в `tasks.txt` между перезапусками
- Логирование действий сервера
- `/health` — эндпоинт для проверки, что сервер жив
- Docker-образ для запуска без локальной настройки окружения
- Тесты на `pytest` + `requests`

## Стек

Python 3, Flask, pytest, Docker

## Установка и запуск

```bash
git clone https://github.com/ltsokay/todo-http-server.git
cd todo-http-server
pip install -r requirements.txt
python app.py
```

Сервер поднимется на `http://127.0.0.1:5000`.

## Запуск в Docker

```bash
docker build -t todo-http-server .
docker run -p 5000:5000 todo-http-server
```

## API

| Метод  | Путь                      | Описание                          |
|--------|---------------------------|------------------------------------|
| POST   | `/tasks`                  | Создать задачу                     |
| GET    | `/tasks`                  | Получить список всех задач         |
| GET    | `/tasks/<id>`             | Получить задачу по id              |
| PUT    | `/tasks/<id>`             | Обновить задачу                    |
| DELETE | `/tasks/<id>`             | Удалить задачу                     |
| POST   | `/tasks/<id>/complete`    | Отметить задачу выполненной        |
| GET    | `/health`                 | Проверка работоспособности сервера |

### Примеры запросов

Создать задачу:
```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Homework", "priority": "normal"}'
```

Получить список задач:
```bash
curl http://127.0.0.1:5000/tasks
```

Отметить задачу выполненной (id=1):
```bash
curl -X POST http://127.0.0.1:5000/tasks/1/complete
```

Удалить задачу (id=1):
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

### Формат задачи

```json
{
  "id": 1,
  "title": "Homework",
  "priority": "normal",
  "isDone": false
}
```

## Тесты

Тесты обращаются к запущенному серверу, поэтому сначала нужно его поднять:

```bash
python app.py
```

В отдельном терминале:
```bash
pytest tests/
```

## Структура проекта

```
todo-http-server/
├── app.py              — маршруты Flask и обработка запросов
├── tasks.py             — модель задачи (dataclass)
├── storage.py            — сохранение и загрузка задач из файла
├── logger.py             — настройка логирования
├── tasks.txt              — файл с сохранёнными задачами (создаётся автоматически)
├── tests/test_api.py       — интеграционные тесты
├── Dockerfile              — сборка Docker-образа
└── requirements.txt         — зависимости проекта
```
