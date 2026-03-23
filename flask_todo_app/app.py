from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "tasks.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
                    )''')
        
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    with get_db_connection() as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return jsonify([dict(t) for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    text = data.get("text", "")
    with get_db_connection() as conn:
        cursor = conn.execute("INSERT INTO tasks (text, completed) VALUES (?, ?)", (text, False))
        task_id = cursor.lastrowid
        conn.commit()
    return jsonify({"id": task_id, "text": text, "completed": False}), 201

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return jsonify({"success": True})

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    with get_db_connection() as conn:
        task = conn.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            return jsonify({"error": "Task not found"}), 404
        new_status = not task["completed"]
        conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
    return jsonify({"id": task_id, "completed": new_status})

@app.route("/api/tasks/clear_completed", methods=["POST"])
def clear_completed():
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE completed = 1")
        conn.commit()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
