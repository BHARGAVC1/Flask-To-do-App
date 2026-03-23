# Antigravity Workspace

This repository contains various small projects and workflows built during my session.

## Flask Todo App (`/flask_todo_app`)
A production-ready, glassmorphism-themed full-stack Todo application built with the **Flask Application Factory** pattern and Blueprints.

### Features
- **Backend Architecture**: Modular Flask app (`config.py`, `run.py`, `app/__init__.py`) with separated route logic (`main.py`, `tasks.py`), custom JSON error handlers, and encapsulated `TaskModel` SQLite operations wrapped under `tasks.db`.
- **Frontend Syncing**: Vanilla JS frontend decoupled into `/app/static` that uses `localStorage` caching synced instantaneously with the backend REST endpoints.
- **Instant Completion Deletion**: Upon clicking the checkbox, tasks receive a brief satisfying strike-through animation before automatically wiping themselves from the UI, logic cache, and backend database—keeping your workspace perfectly clean.
- **Premium Aesthetics**: Smooth micro-animations, ambient colored background orbs, and true glass container styling.

### Running the App
1. Navigate to the project folder:
   ```bash
   cd flask_todo_app
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server using the factory pattern entry point:
   ```bash
   python run.py
   ```
4. Open `http://localhost:5000` in your browser.

## Utilities
- `fibonacci.py`: A Python script containing a Fibonacci generator, covered by `test_fibonacci.py`.
- `.agents/workflows`: Contains custom workflows (e.g., `/generate-unit-tests`) configured for the AI assistant.
