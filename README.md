# Student Task Manager

A small REST API built with **FastAPI** and **SQLite** for managing student tasks. It supports creating, listing, updating, and deleting tasks.

## Features

- Create a new task
- List all tasks
- Update an existing task
- Delete a task
- Input validation with Pydantic
- Persistent storage with SQLite

## Project Structure

```
app/
  __init__.py
  main.py         # FastAPI app and CRUD endpoints
  database.py     # SQLite engine and session
  models.py       # SQLAlchemy Task model
  schemas.py      # Pydantic request/response schemas
tests/
  conftest.py     # Test client and in-memory database
  test_api.py     # API tests
requirements.txt
pytest.ini
README.md
```

## Task Fields

| Field         | Type   | Allowed values                          |
|---------------|--------|-----------------------------------------|
| `id`          | int    | Auto-generated                          |
| `title`       | string | Required, 1–200 characters              |
| `description` | string | Optional, up to 1000 characters         |
| `status`      | string | `pending`, `in_progress`, `completed`   |
| `priority`    | string | `low`, `medium`, `high`                 |

Default status is `pending`. Default priority is `medium`.

## Setup

1. Create and activate a virtual environment.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

From the project root:

```bash
uvicorn app.main:app --reload
```

Then open:

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint            | Description              | Success status |
|--------|---------------------|--------------------------|----------------|
| POST   | `/tasks`            | Create a task            | 201            |
| GET    | `/tasks`            | List all tasks           | 200            |
| PUT    | `/tasks/{task_id}`  | Update a task            | 200            |
| DELETE | `/tasks/{task_id}`  | Delete a task            | 200            |

### Example: create a task

```bash
curl -X POST http://127.0.0.1:8000/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Finish assignment\", \"description\": \"Submit by Friday\", \"status\": \"pending\", \"priority\": \"high\"}"
```

On macOS / Linux:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish assignment", "description": "Submit by Friday", "status": "pending", "priority": "high"}'
```

### Example: list tasks

```bash
curl http://127.0.0.1:8000/tasks
```

### Example: update a task

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### Example: delete a task

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Error Responses

- **400** – PUT body has no fields to update
- **404** – Task id does not exist
- **422** – Invalid input (empty title, unknown status/priority, etc.)

## Run Tests

```bash
pytest
```

Tests use an in-memory SQLite database so they do not change `tasks.db`.
