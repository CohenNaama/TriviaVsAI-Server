"""
Route definitions for question-related endpoints.

This module defines the API endpoints for managing questions,
including retrieval, updating, and viewing question. The routes
utilize the service layer to handle business logic and ensure
request validation.
"""

from flask import Blueprint, request, jsonify
from app.services.question_service import (get_question_by_id_service, get_all_questions_service,
                                           update_question_service, delete_question_service, submit_answer_service)
from app.middleware.decorators import admin_required, json_validator
from app.services.openai_service import create_question_for_session_service

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/questions/next/<int:user_id>/<int:session_id>', methods=['POST'])
def create_next_question(user_id, session_id):
    """
    Generate and return the next question for a game session.

    Args:
        user_id (int): The ID of the user.
        session_id (int): The ID of the game session.

    Returns:
        Response: JSON with the next question and its difficulty (HTTP 201),
        or an error message (HTTP 500).
    """
    try:
        result = create_question_for_session_service(user_id, session_id)
        return jsonify({'status': 'success', 'question': result['question'], 'difficulty': result['difficulty']}), 201
    except Exception as e:
        return jsonify({'status': 'failed', 'message': str(e)}), 500


@question_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id_route(question_id):
    """
    Endpoint to retrieve a specific question by its ID.

    This route handles GET requests to fetch a question's details based on the provided question ID.

    Args:
        question_id (int): The unique identifier of the question to retrieve.

    Returns:
        Response: A JSON response containing the question details and an HTTP status code.
    """
    response, status = get_question_by_id_service(question_id)
    return jsonify(response), status


@question_bp.route('/questions', methods=['GET'])
def get_all_questions_route():
    """
    Endpoint to retrieve all questions.

    This route handles GET requests to fetch a list of all questions available in the system.

    Returns:
        Response: A JSON response containing a list of all questions and an HTTP status code.
    """
    response, status = get_all_questions_service()
    return jsonify(response), status


@question_bp.route('/questions/<int:question_id>', methods=['PATCH'])
@admin_required()
# @json_validator(schema=update_question_schema)
def update_question_route(question_id):
    """
    Endpoint to update a specific question by its ID.

    This route handles PATCH requests to update the details of a question based on the provided question ID.
    It requires admin privileges to access.

    Args:
        question_id (int): The unique identifier of the question to update.
        data (dict): The new data to update the question with, extracted from the request's JSON body.

    Returns:
        Response: A JSON response containing the result of the update operation and an HTTP status code.
    """
    data = request.json
    response, status = update_question_service(question_id, data)
    return jsonify(response), status


@question_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required()
def delete_question_route(question_id):
    """
    Endpoint to delete a specific question by its ID.

    This route handles DELETE requests to remove a question from the system based on the provided question ID.
    It requires admin privileges to access.

    Args:
        question_id (int): The unique identifier of the question to delete.

    Returns:
        Response: A JSON response indicating the result of the delete operation and an HTTP status code.
    """
    response, status = delete_question_service(question_id)
    return jsonify(response), status


@question_bp.route('/users/<int:user_id>/game_sessions/<int:session_id>/submit_answer', methods=['POST'])
def submit_answer_route(user_id, session_id):
    """
    Endpoint to submit an answer for a specific question within a game session.

    This route handles POST requests to record a player's answer to a question within a specific game session.
    The function receives the user's answer, checks its correctness, and updates the game state accordingly.

    Args:
        user_id (int): The unique identifier of the user submitting the answer.
        session_id (int): The unique identifier of the game session.

    Request JSON:
        question_id (int): The unique identifier of the question being answered.
        correct (bool): Whether the answer provided by the player is correct.
        player_response (str): The player's actual answer to the question.

    Returns:
        Response: A JSON response containing the result of the answer submission (e.g., updated game state, feedback)
        and an HTTP status code.
    """
    data = request.json
    question_id = data.get('question_id')
    correct = data.get('correct', False)
    player_response = data.get('player_response')

    response, status = submit_answer_service(session_id, question_id, user_id, correct, player_response)
    return jsonify(response), status
