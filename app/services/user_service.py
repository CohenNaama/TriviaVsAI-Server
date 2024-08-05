from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.middleware.jwt_decorators import json_validator, permission_required
from app.models.user import User, db
from app.models.role import Role
from app.models.claim import Claim
from app.models.userProfile import UserProfile
from .claim_service import create_claims_for_user
from app.middleware.helpers import (user_update_schema, login_schema, save_profile_picture, allowed_file)
from app.logging_config import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


user_service_bp = Blueprint('user_service', __name__)


@user_service_bp.route("/login", methods=["POST"])
@json_validator(schema=login_schema)
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user is None:
            msg = "Username invalid"
            logger.info(msg)
            return jsonify({"message": msg}), 401

        if not user.check_password(password):
            msg = "Password invalid"
            logger.info(msg)
            return jsonify({"message": msg}), 401

        user.last_login = datetime.utcnow()
        db.session.commit()

        user_claims = Claim.query.filter_by(user_id=user.id).all()

        iat = datetime.utcnow()
        exp = iat + timedelta(hours=24)

        additional_claims = {
            'iat': iat,
            "exp": exp,
        }

        all_claims = {claim.type: claim.value for claim in user_claims}
        all_claims.update(additional_claims)

        access_token = create_access_token(identity=user.id, additional_claims=all_claims)

        logger.info(f"User '{username}' logged in successfully.")

        return jsonify(access_token=access_token, token_type='Bearer', iat=iat, exp=exp), 200

    except SQLAlchemyError as e:
        msg = f"Database error during login: {str(e)}"
        logger.error(msg)
        return jsonify({"error": msg}), 500

    except Exception as e:
        msg = f"An unexpected error occurred during login: {str(e)}"
        logger.error(msg)
        return jsonify({"error": msg}), 500


@user_service_bp.route('/users', methods=['POST'])
def create_user():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        profile_picture = request.files.get('profile_picture')
        level = request.form.get('level', type=int, default=1)
        experience_points = request.form.get('experience_points', type=int, default=0)

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            msg = 'Email or username already exists.'
            logger.error(msg)
            return jsonify({'status': 'fail', 'message': msg}), 409

        user_role = Role.query.filter_by(name='Customer').first()
        if not user_role:
            msg = 'User role not found.'
            logger.error(msg)
            return jsonify({'status': 'fail', 'message': msg}), 500

        new_user = User(
            username=username,
            email=email,
            role_id=user_role.id,
            created_at=datetime.utcnow(),
            last_login=None
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.flush()

        filename = 'default.jpg'
        if profile_picture and allowed_file(profile_picture.filename):
            filename = save_profile_picture(profile_picture)

        new_user_profile = UserProfile(
            user_id=new_user.id,
            profile_picture=filename,
            level=level,
            experience_points=experience_points
        )

        db.session.add(new_user_profile)

        create_claims_for_user(
            user_id=new_user.id,
            username=username,
            email=email,
            role_name=user_role.name
        )

        db.session.commit()

        logger.info('New user successfully created.')
        return jsonify({
            'status': 'success',
            'message': 'Successfully created.',
            'data': new_user.to_dict(),
        }), 201

    except SQLAlchemyError as e:
        msg = f'Database error occurred! \nError: {str(e)}'
        logger.error(msg)
        db.session.rollback()
        return jsonify({'status': 'failed', 'message': msg}), 500

    except Exception as e:
        msg = f'An unexpected error occurred! \nError: {str(e)}'
        logger.error(msg)
        db.session.rollback()
        return jsonify({'status': 'failed', 'message': msg}), 500


@user_service_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()

        if not users:
            return jsonify([], 200)
        users_list = [user.to_dict() for user in users]
        return jsonify(users_list), 200

    except Exception as e:
        msg = f'Failed to return users list! \nError: {str(e)}'
        logger.error(msg)
        return jsonify({
            'status': 'failed',
            'message': msg,
        }), 500


@user_service_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            msg = f"User Id:{user_id} does not found"
            logger.warn(msg)
            return jsonify(None, {"message": msg}), 404,

        return jsonify(user.to_dict()), 200

    except Exception as e:
        msg = f"Failed to return user Id:{user_id}. \nError: {str(e)}"
        logger.error(msg)
        return jsonify({
            'status': 'failed',
            'message': msg,
        }), 500


@user_service_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
@permission_required()
@json_validator(schema=user_update_schema)
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user is None:
            msg = f"User ID: {user_id} not found."
            logger.info(msg)
            return jsonify({'status': 'fail', 'message': msg}), 404

        body = request.get_json()
        email = body.get('email')
        password = body.get('password')

        if email:
            existing_user_with_email = User.query.filter_by(email=email).first()
            if existing_user_with_email and existing_user_with_email.id != user_id:
                msg = f"Email '{email}' already exists. Please choose a different email."
                logger.info(msg)
                return jsonify({'status': 'fail', 'message': msg}), 400
            user.email = email

        if password:
            user.set_password(password)

        db.session.commit()

        msg = f"User ID: {user_id} details updated successfully by user ID: {current_user_id}."
        logger.info(msg)
        return jsonify({
            'status': 'success',
            'message': msg,
            'data': user.to_dict(),
        }), 200

    except SQLAlchemyError as e:
        msg = f"Database error during user update: {str(e)}"
        logger.error(msg)
        db.session.rollback()
        return jsonify({'status': 'failed', 'message': msg}), 500

    except Exception as e:
        msg = f"An unexpected error occurred during user update: {str(e)}"
        logger.error(msg)
        return jsonify({'status': 'failed', 'message': msg}), 500


@user_service_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@permission_required()
def delete_user(user_id):
    try:
        current_user = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            msg = f"User ID: {user_id} not found."
            logger.info(msg)
            return jsonify({'status': 'fail', 'message': msg}), 404

        Claim.query.filter_by(user_id=user_id).delete()

        db.session.delete(user)
        db.session.commit()

        msg = f"User ID: {user_id} deleted successfully by user ID: {current_user}."
        logger.info(msg)
        return jsonify({'status': 'success', 'message': msg}), 204

    except IntegrityError as e:
        db.session.rollback()
        msg = f'Deleting user failed due to integrity error: {str(e)}'
        logger.error(msg)
        return jsonify({'status': 'failed', 'message': msg}), 500

    except SQLAlchemyError as e:
        db.session.rollback()
        msg = f'Database error during user deletion: {str(e)}'
        logger.error(msg)
        return jsonify({'status': 'failed', 'message': msg}), 500

    except Exception as e:
        msg = f'An unexpected error occurred during user deletion: {str(e)}'
        logger.error(msg)
        return jsonify({'status': 'failed', 'message': msg}), 500
