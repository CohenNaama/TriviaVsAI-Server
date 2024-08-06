from flask import Blueprint, jsonify, request, send_from_directory, current_app, render_template
from flask_jwt_extended import jwt_required
from app.services.userProfile_service import (
    get_all_profiles,
    get_user_profile_by_id,
    update_user_profile
)
from app.middleware.jwt_decorators import permission_required, form_data_validator
from app.models.user import User
from app.logging_config import logger
from app.schemas.user_schema import user_update_schema

userProfile_bp = Blueprint('userProfile_bp', __name__)


@userProfile_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_users_profiles():
    profiles, status = get_all_profiles()
    return jsonify(profiles), status


@userProfile_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    profile, status = get_user_profile_by_id(user_id)
    return jsonify(profile), status


@userProfile_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@userProfile_bp.route('/profile/<int:user_id>')
def view_profile(user_id):
    user = User.query.get(user_id)
    if user and user.profile:
        logger.debug(f"Profile Picture Filename: {user.profile.profile_picture}")
        return render_template('index.html', profile_picture=user.profile.profile_picture, user_id=user_id)
    else:
        return "User or profile not found", 404


@userProfile_bp.route('/users/<int:user_id>/profile', methods=['PATCH'])
@jwt_required()
@permission_required()
@form_data_validator(user_update_schema)
def update_user_profile_route(user_id):
    response, status = update_user_profile(user_id, request.form, request.files)
    return jsonify(response), status
