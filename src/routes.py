from src import app, db
from src.models.task import Task
from flask import request, jsonify

@app.route("/tasks", methods=["POST"])
def create_task():
    body = request.get_json()
    title = body["title"]
    description = body["description"]

    if title and description:
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "New task created successfully", "id": new_task.id}), 201

    return jsonify({"error": "Credentials is missing or invalid"}), 400


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_object = Task.query.all()

    if tasks_object:
        tasks = [task.to_dict() for task in tasks_object]
        return jsonify({"tasks": tasks, "total_tasks": len(tasks)})
    
    return jsonify({"total_tasks": 0})


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task:
        return jsonify(task.to_dict())

    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    body = request.get_json()
    title = body["title"]
    description = body["description"]

    task = Task.query.get(task_id)

    if task:
        task.title = title
        task.description = description
        db.session.commit()

        return jsonify({"message": "Task updated successfully", "id": task.id})

    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>/completed", methods=["PATCH"])
def update_completed_task(task_id):
    task = Task.query.get(task_id)

    if task:
        task.completed = not task.completed
        db.session.commit()

        if task.completed:
            return jsonify({ "message": "Task marked as complete", "id": task.id })
        
        return jsonify({ "message": "Task marked as incomplete", "id": task.id })
        
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully", "id": task_id})

    return jsonify({"error": "Task not found"}), 404
