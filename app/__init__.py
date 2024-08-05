from flask import Flask
from app.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .logging_config import logger

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    try:
        app = Flask(__name__, template_folder='./templates')
        app.config.from_object(config_class)

        db.init_app(app)
        migrate.init_app(app, db)
        jwt.init_app(app)

        from app.models.user import User
        from app.models.role import Role
        from app.models.claim import Claim
        from app.models.question import Question
        from app.models.category import Category
        from app.models.score import Score
        from app.models.achievement import Achievement
        from app.models.gameSession import GameSession
        from app.models.userProfile import UserProfile

        with app.app_context():
            db.create_all()

        from app.routes.route import main
        from app.services.role_service import role_service_bp
        from app.services.user_service import user_service_bp
        from app.services.userProfile_service import userProfile_service_bp

        app.register_blueprint(main)
        app.register_blueprint(role_service_bp)
        app.register_blueprint(user_service_bp)
        app.register_blueprint(userProfile_service_bp)

        logger.info("Application setup complete.")
        return app

    except Exception as e:
        logger.error(f"Error during application setup: {e}", exc_info=True)
        raise
