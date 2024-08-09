"""
Route definitions for score-related endpoints.

This module defines the API endpoints for managing score, including
creating, retrieving, and listing scores. These routes leverage the service
layer to ensure proper request handling and business logic execution.
"""

from flask import Blueprint, request, jsonify
from app.services.score_service import (
    create_score_service,
    get_score_service,
    get_all_scores_service,
    get_all_scores_of_user_service,
    update_score_service,
    delete_score_service
)
from app.middleware.decorators import admin_required, json_validator
from app.schemas.score_schemas import create_score_schema, update_score_schema

score_bp = Blueprint('score_bp', __name__)


@score_bp.route('/users/<int:user_id>/scores', methods=['POST'])
@admin_required()
@json_validator(schema=create_score_schema)
def create_score(user_id):
    """
    API endpoint to create a new score.

    Returns:
        Response: JSON response with the created score or error message.
    """
    data = request.json
    data['user_id'] = user_id
    response, status = create_score_service(data)
    return jsonify(response), status


@score_bp.route('/users/<int:user_id>/scores/<int:score_id>', methods=['GET'])
def get_score(user_id, score_id):
    """
    API endpoint to retrieve a score by its ID and user ID.

    Returns:
        Response: JSON response with the score or error message.
    """
    response, status = get_score_service(user_id, score_id)
    return jsonify(response), status


@score_bp.route('/users/<int:user_id>/scores', methods=['GET'])
def get_all_scores_of_user(user_id):
    """
    API endpoint to retrieve all scores of the user.

    Returns:
        Response: JSON response with all scores or error message.
    """
    response, status = get_all_scores_of_user_service(user_id)
    return jsonify(response), status


@score_bp.route('/scores', methods=['GET'])
def get_all_scores():
    """
    API endpoint to retrieve all scores.

    Returns:
        Response: JSON response with all scores or error message.
    """
    response, status = get_all_scores_service()
    return jsonify(response), status


@score_bp.route('/users/<int:user_id>/scores/<int:score_id>', methods=['PUT'])
@admin_required()
@json_validator(schema=update_score_schema)
def update_score_route(user_id, score_id):
    """
    API endpoint to update a score.

    Args:
        user_id (int): The ID of the user who owns the score.
        score_id (int): The ID of the score to update.

    Returns:
        Response: JSON response with the updated score or error message.
    """
    data = request.json
    response, status = update_score_service(score_id, user_id, data)
    return jsonify(response), status


@score_bp.route('/users/<int:user_id>/scores/<int:score_id>', methods=['DELETE'])
@admin_required()
def delete_score(user_id, score_id):
    """
    API endpoint to delete a score.

    Returns:
        Response: JSON response with the deletion status or error message.
    """
    response, status = delete_score_service(user_id, score_id)
    return jsonify(response), status
