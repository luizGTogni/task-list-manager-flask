from src import app, tasks
from src.models.task import Task
from flask import request, jsonify

@app.route("/tasks", methods=["POST"])
def create_task():
    title, description = request.get_json()
    id = len(tasks) + 1

    new_task = Task(id=id, title=title, description=description)
    tasks.append(new_task)

    return jsonify({ "message": "New task created successfully" }), 201