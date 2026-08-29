def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Finish assignment",
            "description": "Complete FastAPI CRUD project",
            "status": "pending",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Finish assignment"
    assert data["description"] == "Complete FastAPI CRUD project"
    assert data["status"] == "pending"
    assert data["priority"] == "high"


def test_create_task_uses_defaults(client):
    response = client.post("/tasks", json={"title": "Read notes"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Read notes"
    assert data["description"] is None
    assert data["status"] == "pending"
    assert data["priority"] == "medium"


def test_create_task_invalid_title(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["message"] == "Invalid request data"
    assert data["status_code"] == 422
    assert "details" in data
    assert any("title" in item["field"] for item in data["details"])


def test_create_task_invalid_status(client):
    response = client.post(
        "/tasks",
        json={"title": "Invalid task", "status": "not_a_status"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["status_code"] == 422
    assert any("status" in item["field"] for item in data["details"])


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks(client):
    client.post("/tasks", json={"title": "Task 1", "priority": "low"})
    client.post("/tasks", json={"title": "Task 2", "priority": "high"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Draft report"}).json()
    task_id = created["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "in_progress", "priority": "high"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Draft report"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"


def test_get_task(client):
    created = client.post("/tasks", json={"title": "One task"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "One task"


def test_update_task_not_found(client):
    response = client.put("/tasks/99", json={"title": "Missing"})
    assert response.status_code == 404
    data = response.json()
    assert data == {
        "error": "not_found",
        "message": "Task with id 99 not found",
        "status_code": 404,
    }


def test_update_task_no_fields(client):
    created = client.post("/tasks", json={"title": "Keep as is"}).json()
    response = client.put(f"/tasks/{created['id']}", json={})
    assert response.status_code == 400
    data = response.json()
    assert data == {
        "error": "bad_request",
        "message": "No fields provided for update",
        "status_code": 400,
    }


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Temporary task"}).json()
    task_id = created["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Task with id {task_id} deleted successfully"

    remaining = client.get("/tasks")
    assert remaining.json() == []


def test_delete_task_not_found(client):
    response = client.delete("/tasks/99")
    assert response.status_code == 404
    data = response.json()
    assert data == {
        "error": "not_found",
        "message": "Task with id 99 not found",
        "status_code": 404,
    }


def test_create_then_get_task_by_id(client):
    created = client.post(
        "/tasks",
        json={
            "title": "Lab report",
            "description": "Write the lab report",
            "status": "in_progress",
            "priority": "low",
        },
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "Lab report",
        "description": "Write the lab report",
        "status": "in_progress",
        "priority": "low",
    }


def test_update_all_fields_and_persist(client):
    created = client.post(
        "/tasks",
        json={"title": "Old title", "description": "Old description"},
    ).json()
    task_id = created["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "New description",
            "status": "completed",
            "priority": "low",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "New title",
        "description": "New description",
        "status": "completed",
        "priority": "low",
    }

    stored = client.get(f"/tasks/{task_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == "New title"
    assert stored.json()["description"] == "New description"
    assert stored.json()["status"] == "completed"
    assert stored.json()["priority"] == "low"


def test_deleted_task_cannot_be_retrieved(client):
    keep = client.post("/tasks", json={"title": "Keep this task"}).json()
    remove = client.post("/tasks", json={"title": "Remove this task"}).json()

    delete_response = client.delete(f"/tasks/{remove['id']}")
    assert delete_response.status_code == 200

    missing = client.get(f"/tasks/{remove['id']}")
    assert missing.status_code == 404
    assert missing.json() == {
        "error": "not_found",
        "message": f"Task with id {remove['id']} not found",
        "status_code": 404,
    }

    remaining = client.get("/tasks")
    assert remaining.status_code == 200
    titles = [task["title"] for task in remaining.json()]
    assert titles == ["Keep this task"]

    still_there = client.get(f"/tasks/{keep['id']}")
    assert still_there.status_code == 200
    assert still_there.json()["title"] == "Keep this task"


def test_get_nonexistent_task_when_other_tasks_exist(client):
    client.post("/tasks", json={"title": "Existing task"})

    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["error"] == "not_found"
    assert response.json()["message"] == "Task with id 999 not found"


def test_create_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={"title": "Invalid priority", "priority": "critical"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert data["message"] == "Invalid request data"
    assert any("priority" in item["field"] for item in data["details"])


def test_create_title_too_long(client):
    response = client.post("/tasks", json={"title": "A" * 201})
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert any("title" in item["field"] for item in data["details"])


def test_update_invalid_status(client):
    created = client.post("/tasks", json={"title": "Valid task"}).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"status": "done"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "validation_error"
    assert any("status" in item["field"] for item in data["details"])


def test_put_and_delete_invalid_task_id_type(client):
    put_response = client.put("/tasks/abc", json={"title": "Nope"})
    assert put_response.status_code == 422
    assert put_response.json()["error"] == "validation_error"

    delete_response = client.delete("/tasks/abc")
    assert delete_response.status_code == 422
    assert delete_response.json()["error"] == "validation_error"
