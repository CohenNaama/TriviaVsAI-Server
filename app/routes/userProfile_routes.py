"""
Route definitions for user profile-related endpoints.

This module defines the API endpoints for managing user profiles,
including retrieval, updating, and viewing profiles. The routes
utilize the service layer to handle business logic and ensure
request validation.
"""

from flask import Blueprint, jsonify, request, send_from_directory, current_app, render_template
from flask_jwt_extended import jwt_required
from app.services.userProfile_service import (
    get_all_profiles,
    get_user_profile_by_id,
    update_user_profile
)
from app.middleware.decorators import permission_required, form_data_validator
from app.models.user import User
from app.logging_config import logger
from app.schemas.user_schemas import user_update_schema

userProfile_bp = Blueprint('userProfile_bp', __name__)


@userProfile_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_users_profiles():
    """
    Retrieve all user profiles.

    Requires authentication.

    Returns:
        Response: JSON response with a list of user profiles and HTTP status code.
    """
    profiles, status = get_all_profiles()
    return jsonify(profiles), status


@userProfile_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    """
    Retrieve a user profile by user ID.

    Requires authentication.

    Args:
        user_id (int): ID of the user whose profile to retrieve.

    Returns:
        Response: JSON response with user profile data and HTTP status code.
    """
    profile, status = get_user_profile_by_id(user_id)
    return jsonify(profile), status


@userProfile_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files.

    Args:
        filename (str): Name of the file to serve.

    Returns:
        Response: File response.
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@userProfile_bp.route('/profile/<int:user_id>')
def view_profile(user_id):
    """
    Render user profile page.

    Args:
        user_id (int): ID of the user whose profile to view.

    Returns:
        Response: Rendered HTML page or error message if not found.
    """
    user = User.query.get(user_id)
    if user and user.profile:
        logger.debug(f"Profile Picture Filename: {user.profile.profile_picture}")
        return render_template('index.html',
                               profile_picture=user.profile.profile_picture,
                               user_id=user_id)
    else:
        return "User or profile not found", 404


@userProfile_bp.route('/users/<int:user_id>/profile', methods=['PATCH'])
@jwt_required()
@permission_required()
@form_data_validator(user_update_schema)
def update_user_profile_route(user_id):
    """
    Update a user's profile.

    Requires authentication and permission.

    Args:
        user_id (int): ID of the user whose profile to update.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    response, status = update_user_profile(user_id, request.form, request.files)
    return jsonify(response), status
