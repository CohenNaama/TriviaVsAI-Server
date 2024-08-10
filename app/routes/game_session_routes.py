"""
Route definitions for game session-related endpoints.

This module defines the API endpoints for managing game sessions, including
creating, retrieving, and listing game sessions. These routes leverage the service
layer to ensure proper request handling and business logic execution.
"""

from flask import Blueprint, request, jsonify
from app.services.game_session_service import (
    create_game_session_service,
    get_game_session_service,
    get_all_game_sessions_service,
    get_all_game_sessions_of_user_service,
    update_game_session_service,
    delete_game_session_service
)
from app.middleware.decorators import admin_required, json_validator
from app.schemas.game_session_schemas import create_game_session_schema, update_game_session_schema

game_session_bp = Blueprint('game_session_bp', __name__)


@game_session_bp.route('/users/<int:user_id>/game_sessions', methods=['POST'])
@admin_required()
@json_validator(schema=create_game_session_schema)
def create_game_session(user_id):
    """
    API endpoint to create a new game session.

    Returns:
        Response: JSON response with the created game session or error message.
    """
    data = request.json
    data['user_id'] = user_id
    response, status = create_game_session_service(data)
    return jsonify(response), status


@game_session_bp.route('/users/<int:user_id>/game_sessions/<int:session_id>', methods=['GET'])
def get_game_session(user_id, session_id):
    """
    API endpoint to retrieve a game session by its ID and user ID.

    Returns:
        Response: JSON response with the game session or error message.
    """
    response, status = get_game_session_service(user_id, session_id)
    return jsonify(response), status


@game_session_bp.route('/users/<int:user_id>/game_sessions', methods=['GET'])
def get_all_game_sessions_of_user(user_id):
    """
    API endpoint to retrieve all game sessions of the user.

    Returns:
        Response: JSON response with all game sessions or error message.
    """
    response, status = get_all_game_sessions_of_user_service(user_id)
    return jsonify(response), status


@game_session_bp.route('/game_sessions', methods=['GET'])
def get_all_game_sessions():
    """
    API endpoint to retrieve all game sessions.

    Returns:
        Response: JSON response with all game sessions or error message.
    """
    response, status = get_all_game_sessions_service()
    return jsonify(response), status


@game_session_bp.route('/users/<int:user_id>/game_sessions/<int:session_id>', methods=['PUT'])
@admin_required()
@json_validator(schema=update_game_session_schema)
def update_game_session_route(user_id, session_id):
    """
    API endpoint to update a game session.

    Returns:
        Response: JSON response with the updated game session or error message.
    """
    data = request.json
    response, status = update_game_session_service(session_id, user_id, data)
    return jsonify(response), status


@game_session_bp.route('/users/<int:user_id>/game_sessions/<int:session_id>', methods=['DELETE'])
@admin_required()
def delete_game_session(user_id, session_id):
    """
    API endpoint to delete a game session.

    Returns:
        Response: JSON response with the deletion status or error message.
    """
    response, status = delete_game_session_service(user_id, session_id)
    return jsonify(response), status
