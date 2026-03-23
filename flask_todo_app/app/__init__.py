from flask import Flask
from config import Config
from app.models import init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Database
    init_db(app.config['DB_PATH'])

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.tasks import tasks_bp
    from app.utils.errors import errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(errors_bp)

    return app
