"""
Service layer for managing question-related operations.

This module contains functions to handle question creation, retrieval,
updating, and deletion, utilizing the Data Access Layer (DAL) to
perform database operations.
"""

from app.dal.question_dal import QuestionDAL
from app.logging_config import logger
from sqlalchemy.exc import SQLAlchemyError


def get_question_by_id_service(question_id):
    """
    Service function to retrieve a question by its ID.

    Args:
        question_id (int): The ID of the question.

    Returns:
        tuple: Question data and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        return question.to_dict(), 200
    except SQLAlchemyError as e:
        msg = f"Error retrieving question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_all_questions_service():
    """
    Service function to retrieve all questions.

    Returns:
        tuple: List of questions and status code.
    """
    try:
        questions = QuestionDAL.get_all_questions()
        return [question.to_dict() for question in questions], 200
    except SQLAlchemyError as e:
        msg = f"Error retrieving questions: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def update_question_service(question_id, question_data):
    """
    Service function to update a question.

    Args:
        question_id (int): The ID of the question to update.
        question_data (dict): Data for updating the question.

    Returns:
        tuple: Response message and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        QuestionDAL.update_question(question, **question_data)
        QuestionDAL.commit_changes()
        msg = f"Question ID: {question_id} updated successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 200
    except SQLAlchemyError as e:
        msg = f"Error updating question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def delete_question_service(question_id):
    """
    Service function to delete a question.

    Args:
        question_id (int): The ID of the question to delete.

    Returns:
        tuple: Response message and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        QuestionDAL.delete_question(question)
        msg = f"Question ID: {question_id} deleted successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 200
    except SQLAlchemyError as e:
        msg = f"Error deleting question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500
