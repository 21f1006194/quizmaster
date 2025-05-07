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
    # Create and configure the Flask application
    print("Creating app####")
    app = Flask(__name__)
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

    from app.routes import public_api_bp, admin_bp, user_bp

    app.register_blueprint(public_api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin/api")
    app.register_blueprint(user_bp, url_prefix="/user/api")

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "Internal server error", 500

    return app
