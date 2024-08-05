import logging
from flask import has_request_context, request
from logging.handlers import RotatingFileHandler


logger = logging.getLogger('TriviaVsAILogger')
logger.setLevel(logging.DEBUG)


class NewFormatter(logging.Formatter):
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

# import logging
# from logging.handlers import RotatingFileHandler
# import os
#
#
# def setup_logging():
#     """Setup logging for the application."""
#     # Ensure the logs directory exists
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#
#     # Configure a rotating file handler
#     file_handler = RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
#     ))
#     file_handler.setLevel(logging.INFO)
#
#     # Apply the handler to the root logger
#     logging.getLogger().setLevel(logging.INFO)
#     logging.getLogger().addHandler(file_handler)
