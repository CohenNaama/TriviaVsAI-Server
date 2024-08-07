"""
Initialize the Flask application with configurations, database, and JWT.

This module sets up the Flask app, configures the database and JWT,
and registers all necessary blueprints and error handlers.
"""

from flask import Flask, jsonify
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
    """
    Create and configure the Flask application.

    Args:
        config_class: The configuration class to use for the app.

    Returns:
        app: The configured Flask application instance.
    """
    try:
        app = Flask(__name__, template_folder='./templates')
        app.config.from_object(config_class)

        db.init_app(app)
        migrate.init_app(app, db)
        jwt.init_app(app)

        @app.errorhandler(413)
        def request_entity_too_large(error):
            return jsonify({"message": "The uploaded file is too large. Please upload a file smaller than 16MB."}), 413

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
        from app.routes.user_routes import user_bp
        from app.routes.userProfile_routes import userProfile_bp
        from app.routes.role_routes import role_bp
        from app.routes.category_routes import category_bp
        from app.routes.question_routes import question_bp
        from app.routes.score_routes import score_bp
        from app.routes.openai_routes import openai_bp
        # from app.routes.claude_routes import claude_bp

        app.register_blueprint(main)
        app.register_blueprint(user_bp)
        app.register_blueprint(userProfile_bp)
        app.register_blueprint(role_bp)
        app.register_blueprint(category_bp)
        app.register_blueprint(question_bp)
        app.register_blueprint(score_bp)
        app.register_blueprint(openai_bp)
        # app.register_blueprint(claude_bp)

        logger.info("Application setup complete.")
        return app

    except Exception as e:
        logger.error(f"Error during application setup: {e}", exc_info=True)
        raise
