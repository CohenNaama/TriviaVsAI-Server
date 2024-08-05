from flask import Blueprint, jsonify, request, send_from_directory, current_app, render_template
from flask_jwt_extended import jwt_required
from app.models.userProfile import UserProfile, db
from app.models.user import User
from app.middleware.jwt_decorators import permission_required, multipart_validator
from app.middleware.helpers import save_profile_picture
from app.logging_config import logger
from sqlalchemy.exc import SQLAlchemyError


userProfile_service_bp = Blueprint('userProfile_service_bp', __name__)


@userProfile_service_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_users_profiles():
    try:
        users_profiles = UserProfile.query.all()

        if not users_profiles:
            return jsonify([], 200)
        users_profile_list = [user.to_dict() for user in users_profiles]
        return jsonify(users_profile_list), 200

    except Exception as e:
        msg = f'Failed to return users list! \nError: {str(e)}'
        logger.error(msg)
        return jsonify({
            'status': 'failed',
            'message': msg,
        }), 500


@userProfile_service_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile_by_id(user_id):
    try:
        user_profile = UserProfile.query.filter_by(id=user_id).first()
        if not user_profile:
            msg = f"User Id:{user_id} does not found"
            logger.warn(msg)
            return jsonify(None, {"message": msg}), 404,

        return jsonify(user_profile.to_dict()), 200

    except Exception as e:
        msg = f"Failed to return user Id:{user_id}. \nError: {str(e)}"
        logger.error(msg)
        return jsonify({
            'status': 'failed',
            'message': msg,
        }), 500


@userProfile_service_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@userProfile_service_bp.route('/profile/<int:user_id>')
def view_profile(user_id):
    user = User.query.get(user_id)
    if user and user.profile:
        print(f"Profile Picture Filename: {user.profile.profile_picture}")
        return render_template('index.html', profile_picture=user.profile.profile_picture, user_id=user_id)
    else:
        return "User or profile not found", 404


@userProfile_service_bp.route('/users/<int:user_id>/profile', methods=['PATCH'])
@jwt_required()
@permission_required()
@multipart_validator(['profile_picture'])
def update_user_profile(user_id):
    try:
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"status": "fail", "message": "User not found"}), 404

        profile_picture = request.files.get('profile_picture')
        level = request.form.get('level', type=int)
        experience_points = request.form.get('experience_points', type=int)

        if profile_picture:
            filename = save_profile_picture(profile_picture)
            if filename:
                user.profile.profile_picture = filename

        if level is not None:
            user.profile.level = level
        if experience_points is not None:
            user.profile.experience_points = experience_points

        db.session.commit()

        msg = f"User ID: {user_id} details updated successfully."
        logger.info(msg)
        return jsonify({
            'status': 'success',
            'message': msg,
            'data': user.profile.to_dict(),
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        msg = f"Database error during user update: {str(e)}"
        logger.error(msg)
        return jsonify({'status': 'failed', 'message': msg}), 500

    except Exception as e:
        msg = f"An unexpected error occurred during user update: {str(e)}"
        logger.error(msg)
        return jsonify({'status': 'failed', 'message': msg}), 500
