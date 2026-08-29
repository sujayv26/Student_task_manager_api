from app.database import get_db
from app.main import app


def test_get_task_not_found(client):
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert "detail" not in response.json()
    assert response.json() == {
        "success": False,
        "message": "Task not found",
        "data": None,
    }


def test_get_deleted_task_returns_not_found(client):
    created = client.post("/tasks", json={"title": "Delete me"}).json()
    task_id = created["data"]["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {
        "success": True,
        "message": "Task deleted successfully",
        "data": None,
    }

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404
    assert get_resp.json() == {
        "success": False,
        "message": "Task not found",
        "data": None,
    }


def test_put_invalid_priority(client):
    created = client.post("/tasks", json={"title": "Valid task"}).json()
    response = client.put(f"/tasks/{created['data']['id']}", json={"priority": "urgent"})
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "message": "Validation error",
        "data": None,
    }


def test_put_invalid_title(client):
    created = client.post("/tasks", json={"title": "Valid task"}).json()
    response = client.put(f"/tasks/{created['data']['id']}", json={"title": ""})
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "message": "Validation error",
        "data": None,
    }


def test_invalid_task_id_type(client):
    response = client.get("/tasks/abc")
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "message": "Validation error",
        "data": None,
    }


def test_missing_title_on_create(client):
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "message": "Validation error",
        "data": None,
    }


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
        "success": False,
        "message": "An unexpected error occurred. Please try again later.",
        "data": None,
    }
    body = str(data).lower()
    assert secret.lower() not in body
    assert "traceback" not in body
    assert "runtimeerror" not in body
    assert "detail" not in data
