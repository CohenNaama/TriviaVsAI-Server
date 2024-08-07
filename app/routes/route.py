from flask import Blueprint, render_template
from sqlalchemy import text
from app import db

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """
    Render the home page.

    Returns:
        Response: Rendered HTML page for the home route.
    """
    return render_template('index.html')
