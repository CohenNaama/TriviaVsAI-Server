"""
Route definitions for achievement-related endpoints.

This module defines the API endpoints for managing achievements, including
creating, retrieving, and listing achievements. These routes leverage the service
layer to ensure proper request handling and business logic execution.
"""

from flask import Blueprint, request, jsonify
from app.services.achievement_service import (
    create_achievement_service,
    get_achievement_service,
    get_all_achievements_service,
    get_all_achievements_of_user_service,
    update_achievement_service,
    delete_achievement_service
)
from app.middleware.decorators import admin_required, json_validator
from app.schemas.achievement_schemas import create_achievement_schema, update_achievement_schema

achievement_bp = Blueprint('achievement_bp', __name__)


@achievement_bp.route('/users/<int:user_id>/achievements', methods=['POST'])
@admin_required()
@json_validator(schema=create_achievement_schema)
def create_achievement(user_id):
    """
    API endpoint to create a new achievement.

    Returns:
        Response: JSON response with the created achievement or error message.
    """
    data = request.json
    data['user_id'] = user_id
    response, status = create_achievement_service(data)
    return jsonify(response), status


@achievement_bp.route('/users/<int:user_id>/achievements/<int:achievement_id>', methods=['GET'])
def get_achievement(user_id, achievement_id):
    """
    API endpoint to retrieve an achievement by its ID and user ID.

    Returns:
        Response: JSON response with the achievement or error message.
    """
    response, status = get_achievement_service(user_id, achievement_id)
    return jsonify(response), status


@achievement_bp.route('/users/<int:user_id>/achievements', methods=['GET'])
def get_all_achievements_of_user(user_id):
    """
    API endpoint to retrieve all achievements of the user.

    Returns:
        Response: JSON response with all achievements or error message.
    """
    response, status = get_all_achievements_of_user_service(user_id)
    return jsonify(response), status


@achievement_bp.route('/achievements', methods=['GET'])
def get_all_achievements():
    """
    API endpoint to retrieve all achievements.

    Returns:
        Response: JSON response with all achievements or error message.
    """
    response, status = get_all_achievements_service()
    return jsonify(response), status


@achievement_bp.route('/users/<int:user_id>/achievements/<int:achievement_id>', methods=['PATCH'])
@admin_required()
@json_validator(schema=update_achievement_schema)
def update_achievement_route(user_id, achievement_id):
    """
    API endpoint to update an achievement.

    Returns:
        Response: JSON response with the updated achievement or error message.
    """
    data = request.json
    response, status = update_achievement_service(achievement_id, user_id, data)
    return jsonify(response), status


@achievement_bp.route('/users/<int:user_id>/achievements/<int:achievement_id>', methods=['DELETE'])
@admin_required()
def delete_achievement(user_id, achievement_id):
    """
    API endpoint to delete an achievement.

    Returns:
        Response: JSON response with the deletion status or error message.
    """
    response, status = delete_achievement_service(user_id, achievement_id)
    return jsonify(response), status
