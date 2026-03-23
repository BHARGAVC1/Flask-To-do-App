from flask import Blueprint, request, jsonify, current_app
from app.models import TaskModel

tasks_bp = Blueprint('tasks', __name__)

def get_task_model():
    return TaskModel(current_app.config['DB_PATH'])

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    return jsonify(get_task_model().get_all())

@tasks_bp.route("", methods=["POST"])
def add_task():
    data = request.get_json()
    text = data.get("text", "")
    new_task = get_task_model().add(text)
    return jsonify(new_task), 201

@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    get_task_model().delete(task_id)
    return jsonify({"success": True})

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    result = get_task_model().toggle(task_id)
    if not result:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(result)

@tasks_bp.route("/clear_completed", methods=["POST"])
def clear_completed():
    get_task_model().clear_completed()
    return jsonify({"success": True})
