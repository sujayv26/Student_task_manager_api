from app.database import get_db
from app.main import app


def test_get_task_not_found(client):
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert "detail" not in response.json()
    assert response.json() == {
        "error": "not_found",
        "message": "Task with id 99 not found",
        "status_code": 404,
    }


def test_put_invalid_priority(client):
    created = client.post("/tasks", json={"title": "Valid task"}).json()
    response = client.put(f"/tasks/{created['id']}", json={"priority": "urgent"})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["message"] == "Invalid request data"
    assert data["status_code"] == 422
    assert isinstance(data["details"], list)
    assert data["details"]


def test_put_invalid_title(client):
    created = client.post("/tasks", json={"title": "Valid task"}).json()
    response = client.put(f"/tasks/{created['id']}", json={"title": ""})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert any("title" in item["field"] for item in data["details"])


def test_invalid_task_id_type(client):
    response = client.get("/tasks/abc")
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["message"] == "Invalid request data"
    assert data["status_code"] == 422


def test_missing_title_on_create(client):
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert "details" in data
    assert any("title" in item["field"] for item in data["details"])


def test_unexpected_error_hides_internal_details(client):
    secret = "sqlite:///secret-internal.db leaked traceback"

    def broken_get_db():
        raise RuntimeError(secret)
        yield

    app.dependency_overrides[get_db] = broken_get_db
    try:
        response = client.get("/tasks")
    finally:
        del app.dependency_overrides[get_db]

    assert response.status_code == 500
    data = response.json()
    assert data == {
        "error": "internal_server_error",
        "message": "An unexpected error occurred. Please try again later.",
        "status_code": 500,
    }
    body = str(data).lower()
    assert secret.lower() not in body
    assert "traceback" not in body
    assert "runtimeerror" not in body
    assert "detail" not in data
