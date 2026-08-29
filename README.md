# Student Task Manager API

A small REST API for managing student tasks, built using FastAPI, SQLite, SQLAlchemy, Pydantic, and Pytest.

This project was developed as part of **Automation in Software Development – Unit 2 – Assignment A1: AI Coding Assistant Practicum**.

## Project Overview

The Student Task Manager API provides CRUD operations for managing student tasks.

Each task contains:

- `id`
- `title`
- `description`
- `status`
- `priority`

The API includes input validation, error handling, database persistence, and automated tests.

## AI Coding Assistant Used

**Tool:** Antigravity AI Coding Assistant

The project was developed using an AI-powered coding assistant instead of GitHub Copilot, as required by the assignment.

Three prompt engineering techniques were applied:

| Technique | Usage |
|-----------|-------|
| **Zero-Shot Prompting** | Used for the initial project structure, CRUD endpoints, database integration, validation, and tests without providing examples. |
| **Few-Shot Prompting** | Used to establish consistent API response and error formats by providing examples of the expected output structure. |
| **Chain-of-Thought Prompting** | Used for step-by-step debugging of task deletion, partial updates, and database consistency edge cases. |

Detailed prompts, tool responses, evaluations, and screenshots are available in the `docs/` folder.

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Pytest
- Uvicorn
- Git & GitHub

## Project Structure

```text
Student_task_manager_api/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── errors.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_errors.py
│
├── docs/
│   └── ...
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sujayv26/Student_task_manager_api.git
```

### 2. Navigate to the project

```bash
cd Student_task_manager_api
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## API Endpoints

| Method   | Endpoint           | Description              |
| -------- | ------------------ | ------------------------ |
| `POST`   | `/tasks`           | Create a task            |
| `GET`    | `/tasks`           | Retrieve all tasks       |
| `GET`    | `/tasks/{task_id}` | Retrieve a specific task |
| `PUT`    | `/tasks/{task_id}` | Update a task            |
| `DELETE` | `/tasks/{task_id}` | Delete a task            |

## Task Validation

### Status

Supported values:

```text
pending
in_progress
completed
```

### Priority

Supported values:

```text
low
medium
high
```

Invalid values and invalid input are rejected through validation.

## Example Request

### Create a Task

```http
POST /tasks
```

```json
{
  "title": "Complete assignment",
  "description": "Finish the AI Coding Assistant assignment",
  "status": "pending",
  "priority": "high"
}
```

## Example Response

```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {
    "id": 1,
    "title": "Complete assignment",
    "description": "Finish the AI Coding Assistant assignment",
    "status": "pending",
    "priority": "high"
  }
}
```

## Testing

Run the complete test suite:

```bash
pytest
```

The tests cover:

* CRUD operations
* Input validation
* Error handling
* Missing task scenarios
* Partial task updates
* Task deletion
* Database consistency


## Version Control

The project was developed incrementally using Git.

Separate commits were created during different stages of development to maintain the development history and demonstrate the progression of the AI-assisted implementation.

## Author

**Sujay V**

B.Tech Computer Science Engineering  
AI-driven DevOps
