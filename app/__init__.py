from flask import Flask
from app.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='./templates')
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes.route import main
    app.register_blueprint(main)

    return app
