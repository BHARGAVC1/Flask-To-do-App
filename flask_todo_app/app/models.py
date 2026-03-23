import sqlite3

def init_db(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
                    )''')

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class TaskModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_all(self):
        with get_db_connection(self.db_path) as conn:
            tasks = conn.execute("SELECT * FROM tasks").fetchall()
        return [dict(t) for t in tasks]

    def add(self, text):
        with get_db_connection(self.db_path) as conn:
            cursor = conn.execute("INSERT INTO tasks (text, completed) VALUES (?, ?)", (text, False))
            task_id = cursor.lastrowid
            conn.commit()
        return {"id": task_id, "text": text, "completed": False}

    def delete(self, task_id):
        with get_db_connection(self.db_path) as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    def toggle(self, task_id):
        with get_db_connection(self.db_path) as conn:
            task = conn.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if not task:
                return None
            new_status = not task["completed"]
            conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
            conn.commit()
            return {"id": task_id, "completed": new_status}

    def clear_completed(self):
        with get_db_connection(self.db_path) as conn:
            conn.execute("DELETE FROM tasks WHERE completed = 1")
            conn.commit()
