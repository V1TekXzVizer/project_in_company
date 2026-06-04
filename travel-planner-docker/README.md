# Travel Planner API

API для планирования путешествий с интеграцией Art Institute of Chicago API.

## Технологии
- FastAPI
- SQLite (SQLAlchemy)
- Docker / docker-compose
- HTTPX

## Запуск

### Через Docker (рекомендуется)
```bash
docker-compose up --build
```

### Локально (без Docker)
```bash
pip install -r requirements.txt
python -m app.main
```

## API Endpoints

### Проекты
- `GET /projects` - Список проектов
- `POST /projects` - Создать проект
- `GET /projects/{id}` - Детали проекта
- `PUT /projects/{id}` - Обновить проект
- `DELETE /projects/{id}` - Удалить проект

### Места
- `GET /projects/{project_id}/places` - Список мест в проекте
- `POST /projects/{project_id}/places` - Добавить место
- `GET /projects/{project_id}/places/{place_id}` - Детали места
- `PUT /projects/{project_id}/places/{place_id}` - Обновить место
- `DELETE /projects/{project_id}/places/{place_id}` - Удалить место

## Документация
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Пример запроса
POST /projects
{
  "name": "Поездка в Чикаго",
  "places": [
    {"external_id": "129884"}
  ]
}

Переменные окружения

DATABASE_URL (опционально, по умолчанию sqlite:///./travel.db)

Валидации
Максимум 10 мест на проект

Нельзя добавить одно место дважды

Нельзя удалить проект с посещёнными местами

Проверка мест через Art Institute API