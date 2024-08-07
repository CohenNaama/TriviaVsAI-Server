"""
Configuration for application logging.

This module sets up the logging configuration to output logs
to both console and file with specific formatting and rotation
policies.
"""

import logging
from flask import has_request_context, request
from logging.handlers import RotatingFileHandler


logger = logging.getLogger('TriviaVsAILogger')
logger.setLevel(logging.DEBUG)


class NewFormatter(logging.Formatter):
    """
    Custom logging formatter for the Trivia Vs AI application.

    This formatter adds the URL of the request to the log record if the request context is available.
    """
    def format(self, record):
        record.name = 'Trivia Vs AI'
        if has_request_context():
            record.url = request.url
        else:
            record.url = None
        record.levelname = record.levelname
        return super().format(record)


logFormatter = NewFormatter("%(asctime)s - %(url)s - %(levelname)s - %(name)s >>> %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

fileHandler = RotatingFileHandler("logs.log", backupCount=100, maxBytes=100000)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
