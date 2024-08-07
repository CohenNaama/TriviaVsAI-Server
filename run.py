"""
Entry point for running the Flask application.

This module creates and runs the Flask application instance.
"""

from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run()
