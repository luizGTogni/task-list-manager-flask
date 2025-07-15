import pytest
import requests

BASE_URL = "http://localhost:5000/"
tasks = []


def test_create_task():
    new_task_data = {"title": "Task Title", "description": "Test Description"}

    res = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    res_json = res.json()

    assert res.status_code == 201
    assert "message" in res_json
    assert "id" in res_json
    tasks.append(res_json["id"])


def test_get_tasks():
    res = requests.get(f"{BASE_URL}/tasks")
    res_json = res.json()

    assert res.status_code == 200
    assert "tasks" in res_json
    assert "total_tasks" in res_json


def test_get_task():
    if tasks:
        task_id = tasks[0]
        res = requests.get(f"{BASE_URL}/tasks/{task_id}")
        res_json = res.json()

        assert res.status_code == 200
        assert task_id == res_json["id"]


def test_update_task():
    update_task_data = {
        "title": "Update Title",
        "description": "Update Description",
        "completed": True,
    }

    if tasks:
        task_id = tasks[0]
        res = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_task_data)
        res_json = res.json()
        res_get_task = requests.get(f"{BASE_URL}/tasks/{task_id}").json()

        assert res.status_code == 200
        assert "id" in res_json
        assert task_id == res_json["id"]
        assert res_get_task["title"] == update_task_data["title"]
        assert res_get_task["description"] == update_task_data["description"]
        assert res_get_task["completed"] == update_task_data["completed"]


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        res = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        res_json = res.json()
        res_delete_task = requests.get(f"{BASE_URL}/tasks/{task_id}")

        assert res.status_code == 200
        assert "id" in res_json
        assert task_id == res_json["id"]
        assert res_delete_task.status_code == 404
