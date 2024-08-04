from flask import Blueprint, render_template
from sqlalchemy import text
from app import db

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/test_db')
def test_db():
    try:
        # Wrap the raw SQL in a text() function
        db.session.execute(text('SELECT 1'))
        return "Database connected successfully!", 200
    except Exception as e:
        return f"Database connection failed: {e}", 500
