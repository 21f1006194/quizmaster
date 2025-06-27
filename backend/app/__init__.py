import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import LoginManager
from app.config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt_manager = JWTManager()


def create_app(config_class=Config):
    # Get the absolute path to the backend folder (one level up from app)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_folder = os.path.join(backend_dir, "static")

    app = Flask(__name__, static_folder=static_folder, static_url_path="/static")
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True)

    # Initialize extensions with the app context
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt_manager.init_app(app)

    login_manager.login_view = "public.login"
    login_manager.login_message = "Please log in to access this page"

    with app.app_context():
        from app.models import User

    @app.shell_context_processor
    def make_shell_context():

        return {
            "db": db,
            "User": User,
        }

    from app.routes import public_api_bp, admin_bp, user_bp, upload_bp

    app.register_blueprint(public_api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin/api")
    app.register_blueprint(user_bp, url_prefix="/user/api")
    app.register_blueprint(upload_bp, url_prefix="/upload/api")

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "Internal server error", 500

    return app
