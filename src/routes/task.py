from src import app, db, login_manager
from src.models.task import Task
from flask import request, jsonify
from flask_login import login_required, current_user

@app.route("/tasks", methods=["POST"])
@login_required
def create_task():
    body = request.get_json()
    title = body["title"]
    description = body["description"]

    if title and description:
        new_task = Task(title=title, description=description, user_owner=current_user.id)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "New task created successfully", "id": new_task.id}), 201

    return jsonify({"error": "Credentials is missing or invalid"}), 400


@app.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks_object = Task.query.filter_by(user_owner=current_user.id).all()

    if tasks_object:
        tasks = [task.to_dict() for task in tasks_object]
        return jsonify({"tasks": tasks, "total_tasks": len(tasks)})
    
    return jsonify({"total_tasks": 0})


@app.route("/tasks/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id):
    task = Task.query.get(task_id)

    if task:
        if task.user_owner == current_user.id:
            return jsonify(task.to_dict())
        
        return login_manager.unauthorized()
    
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    body = request.get_json()
    title = body["title"]
    description = body["description"]

    task = Task.query.get(task_id)

    if task:
        if task.user_owner == current_user.id:
            task.title = title
            task.description = description
            db.session.commit()

            return jsonify({"message": "Task updated successfully", "id": task.id})
        return login_manager.unauthorized()

    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>/completed", methods=["PATCH"])
@login_required
def update_completed_task(task_id):
    task = Task.query.get(task_id)

    if task:
        if task.user_owner == current_user.id:
            task.completed = not task.completed
            db.session.commit()

            if task.completed:
                return jsonify({ "message": "Task marked as complete", "id": task.id })
            return jsonify({ "message": "Task marked as incomplete", "id": task.id })
        
        return login_manager.unauthorized()
    
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task:
        if task.user_owner == current_user.id:
            db.session.delete(task)
            db.session.commit()

            return jsonify({"message": "Task deleted successfully", "id": task_id})
        return login_manager.unauthorized()

    return jsonify({"error": "Task not found"}), 404
