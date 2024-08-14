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
    API endpoint to create the next AI-generated question for the user in a specific session, adjusting difficulty as needed.

    Returns:
        Response: JSON response with the next question or error message.
    """
    try:
        result = create_question_for_session_service(user_id, session_id)
        return jsonify({'status': 'success', 'question': result['question'], 'difficulty': result['difficulty']}), 201
    except Exception as e:
        return jsonify({'status': 'failed', 'message': str(e)}), 500


@question_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id_route(question_id):
    response, status = get_question_by_id_service(question_id)
    return jsonify(response), status


@question_bp.route('/questions', methods=['GET'])
def get_all_questions_route():
    response, status = get_all_questions_service()
    return jsonify(response), status


@question_bp.route('/questions/<int:question_id>', methods=['PATCH'])
@admin_required()
# @json_validator(schema=update_question_schema)
def update_question_route(question_id):
    data = request.json
    response, status = update_question_service(question_id, data)
    return jsonify(response), status


@question_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required()
def delete_question_route(question_id):
    response, status = delete_question_service(question_id)
    return jsonify(response), status


@question_bp.route('/users/<int:user_id>/game_sessions/<int:session_id>/submit_answer', methods=['POST'])
def submit_answer_route(user_id, session_id):
    """
    API endpoint to submit an answer and update the success rate and streaks.

    Returns:
        Response: JSON response indicating success or failure.
    """
    data = request.json
    question_id = data.get('question_id')
    correct = data.get('correct', False)

    response, status = submit_answer_service(session_id, question_id, user_id, correct)
    return jsonify(response), status
