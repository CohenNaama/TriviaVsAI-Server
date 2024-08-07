"""
Route definitions for user-related endpoints.

This module defines the API endpoints for managing users, including
user creation, login, retrieval, updating, and deletion. These routes
utilize the service layer for business logic and ensure proper request
validation and authentication.
"""

from app.services.user_service import login as login_service
from flask_jwt_extended import jwt_required
from app.middleware.decorators import json_validator, permission_required, form_data_validator
from app.schemas.user_schema import login_schema, user_create_schema, user_update_schema
from flask import Blueprint, request, jsonify
from app.services.user_service import (
    create_user as create_user_service,
    get_users as get_users_service,
    get_user_by_id as get_user_by_id_service,
    update_user as update_user_service,
    delete_user as delete_user_service
)


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
@json_validator(login_schema)
def login():
    """
    Handle user login.

    Validates login credentials and returns a JWT access token if successful.

    Returns:
        Response: JSON response with access token and HTTP status code.
    """
    data = request.json
    response, status = login_service(data)
    return jsonify(response), status


@user_bp.route('/users', methods=['POST'])
@form_data_validator(user_create_schema)
def create_user():
    """
    Create a new user.

    Validates and processes form data to create a new user account.

    Returns:
        Response: JSON response with user data and HTTP status code.
    """
    data = request.form.to_dict()
    files = request.files
    response, status = create_user_service(data, files)
    return jsonify(response), status


@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Retrieve all users.

    Requires authentication.

    Returns:
        Response: JSON response with a list of users and HTTP status code.
    """
    response, status = get_users_service()
    return jsonify(response), status


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    """
    Retrieve a user by ID.

    Requires authentication.

    Args:
        user_id (int): ID of the user to retrieve.

    Returns:
        Response: JSON response with user data and HTTP status code.
    """
    response, status = get_user_by_id_service(user_id)
    return jsonify(response), status


@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
@permission_required()
@json_validator(user_update_schema)
def update_user(user_id):
    """
    Update a user's information.

    Requires authentication and permission.

    Args:
        user_id (int): ID of the user to update.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    data = request.json
    response, status = update_user_service(user_id, data)
    return jsonify(response), status


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@permission_required()
def delete_user(user_id):
    """
    Delete a user by ID.

    Requires authentication and permission.

    Args:
        user_id (int): ID of the user to delete.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    response, status = delete_user_service(user_id)
    return jsonify(response), status
