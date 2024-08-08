"""
Route definitions for question-related endpoints.

This module defines the API endpoints for managing questions,
including retrieval, updating, and viewing question. The routes
utilize the service layer to handle business logic and ensure
request validation.
"""

from flask import Blueprint, request, jsonify
from app.services.question_service import (create_question_with_ai, get_question_by_id_service,
                                           get_all_questions_service, update_question_service, delete_question_service)
from app.middleware.decorators import admin_required, json_validator

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/questions/ai', methods=['POST'])
@admin_required()
def create_question_route():
    """
    API endpoint to create a question using AI.

    Returns:
        Response: JSON response with the created question or error message.
    """
    data = request.json
    response, status = create_question_with_ai(data)
    return jsonify(response), status


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
