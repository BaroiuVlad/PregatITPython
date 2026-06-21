import pytest
from fastapi.testclient import TestClient
from api import app
from db_handler import get_db_connection

# TestClient allows us to test the API without manually starting the server
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM tasks")
        conn.commit()
    conn.close()


def test_create_task():

    payload = {"title": "Test Task", "owner": "Vladut", "description": "Verify coverage"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


def test_get_task_not_found():

    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_workflow_transition():

    # First, create a task
    res = client.post("/tasks", json={"title": "Status Test", "owner": "Admin"})
    task_id = res.json()["id"]

    # Change status to IN_PROGRESS
    response = client.post(f"/tasks/{task_id}/status", json={"new_status": "IN_PROGRESS"})
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_delete_task_restful():

    res = client.post("/tasks", json={"title": "Delete Me", "owner": "User"})
    task_id = res.json()["id"]

    # Perform Delete
    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204

    # Confirm it is gone
    verify_res = client.get(f"/tasks/{task_id}")
    assert verify_res.status_code == 404