import pytest
import requests

BASE_URL = "http://localhost:5000/"
tasks = []

@pytest.fixture(scope="session")
def logged_session():
    session = requests.Session()

    payload = {"username": "toogni", "password": "123456"}
    response = session.post(f"{BASE_URL}/login", json=payload)

    assert response.status_code == 200
    return session

def test_create_task(logged_session):
    new_task_data = {"title": "Task Title", "description": "Test Description"}

    res = logged_session.post(f"{BASE_URL}/tasks", json=new_task_data)
    res_json = res.json()

    assert res.status_code == 201
    assert "message" in res_json
    assert "id" in res_json
    tasks.append(res_json["id"])


def test_get_tasks(logged_session):
    res = logged_session.get(f"{BASE_URL}/tasks")
    res_json = res.json()

    assert res.status_code == 200
    assert "tasks" in res_json
    assert "total_tasks" in res_json


def test_get_task(logged_session):
    if tasks:
        task_id = tasks[0]
        res = logged_session.get(f"{BASE_URL}/tasks/{task_id}")
        res_json = res.json()

        assert res.status_code == 200
        assert task_id == res_json["id"]


def test_update_task(logged_session):
    update_task_data = {
        "title": "Update Title",
        "description": "Update Description"
    }

    if tasks:
        task_id = tasks[0]
        res = logged_session.put(f"{BASE_URL}/tasks/{task_id}", json=update_task_data)
        res_json = res.json()
        res_get_task = logged_session.get(f"{BASE_URL}/tasks/{task_id}").json()

        assert res.status_code == 200
        assert "id" in res_json
        assert task_id == res_json["id"]
        assert res_get_task["title"] == update_task_data["title"]
        assert res_get_task["description"] == update_task_data["description"]

def test_update_completed_task(logged_session):
    if tasks:
        task_id = tasks[0]
        res = logged_session.patch(f"{BASE_URL}/tasks/{task_id}/completed")
        res_json = res.json()
        res_get_task = logged_session.get(f"{BASE_URL}/tasks/{task_id}").json()

        assert res.status_code == 200
        assert "id" in res_json
        assert task_id == res_json["id"]
        assert res_get_task["completed"] == True

        res = logged_session.patch(f"{BASE_URL}/tasks/{task_id}/completed")
        res_json = res.json()
        res_get_task = logged_session.get(f"{BASE_URL}/tasks/{task_id}").json()

        assert res_get_task["completed"] == False

def test_delete_task(logged_session):
    if tasks:
        task_id = tasks[0]
        res = logged_session.delete(f"{BASE_URL}/tasks/{task_id}")
        res_json = res.json()
        res_delete_task = logged_session.get(f"{BASE_URL}/tasks/{task_id}")

        assert res.status_code == 200
        assert "id" in res_json
        assert task_id == res_json["id"]
        assert res_delete_task.status_code == 404
