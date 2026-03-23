import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-123'
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks.db')
