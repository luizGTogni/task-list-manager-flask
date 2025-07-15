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
    return jsonify({ "tasks": list_tasks, "total_tasks": len(tasks) })

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = [task for task in tasks if task.id == task_id]

    if len(task) > 0:
        return jsonify(task[0].to_dict())

    return jsonify({ "message": "Not found task" }), 404

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = [task for task in tasks if task.id == task_id]

    if len(task) > 0:
        task[0].title = data["title"]
        task[0].description = data["description"]
        task[0].completed = data["completed"]
        
        return jsonify({ "message": "Task updated successfully" })

    return jsonify({ "message": "Not found task" }), 404