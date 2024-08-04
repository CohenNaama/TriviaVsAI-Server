from flask import Flask
from app.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='./templates')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.user import User
    from .models.role import Role
    from .models.claim import Claim
    from .models.question import Question
    from .models.category import Category
    from .models.score import Score
    from .models.achievement import Achievement
    from .models.gameSession import GameSession

    with app.app_context():
        db.create_all()

    from .routes.route import main
    app.register_blueprint(main)

    return app
