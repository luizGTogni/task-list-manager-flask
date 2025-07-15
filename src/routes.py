from src import app, tasks
from src.models.task import Task
from flask import request, jsonify

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    id = len(tasks) + 1

    new_task = Task(id=id, title=data['title'], description=data['description'])
    tasks.append(new_task)

    return jsonify({ "message": "New task created successfully" }), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    list_tasks = [task.to_dict() for task in tasks]
    return jsonify({ "tasks": list_tasks, "total_tasks": len(tasks) }), 200