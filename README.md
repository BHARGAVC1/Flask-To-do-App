# Antigravity Workspace

This repository contains various small projects and workflows built during my session.

## Flask Todo App (`/flask_todo_app`)
A premium, glassmorphism-themed Todo application built with:
- **Backend**: Flask + SQLite Database `tasks.db`.
- **Frontend**: Vanilla JS, LocalStorage caching, and beautiful customized CSS graphics.
- **Features**: Task Filters (All, Pending, Completed), Checkbox strike-throughs, Safe deletions, and real-time database synchronization from the browser.

### Running the App
1. Navigate to the project folder:
   ```bash
   cd flask_todo_app
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser.

## Utilities
- `fibonacci.py`: A Python script containing a Fibonacci generator, covered by `test_fibonacci.py`.
- `.agents/workflows`: Contains custom workflows (e.g., `/generate-unit-tests`) configured for the AI assistant.
