"""
Service layer for managing user-related operations.

This module contains functions to handle user creation, retrieval,
updating, and deletion, utilizing the Data Access Layer (DAL) to
perform database operations.
"""

from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.dal.user_dal import UserDAL
from app.models.claim import Claim
from app.models.userProfile import UserProfile
from .claim_service import create_claims_for_user
from app.middleware.helpers import save_profile_picture, allowed_file
from app.logging_config import logger


def login(data):
    """
    Authenticate a user and generate an access token.

    Args:
        data (dict): A dictionary containing username and password.

    Returns:
        tuple: A response containing an access token and an HTTP status code.
    """
    try:
        username = data.get("username")
        password = data.get("password")

        user = UserDAL.get_user_by_username(username)

        if user is None:
            msg = "Username invalid"
            logger.info(msg)
            return {"message": msg}, 401

        if not user.check_password(password):
            msg = "Password invalid"
            logger.info(msg)
            return {"message": msg}, 401

        user.last_login = datetime.utcnow()
        UserDAL.commit_changes()

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

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "iat": iat.isoformat(),
            "exp": exp.isoformat()
        }, 200

    except Exception as e:
        msg = f"An unexpected error occurred during login: {str(e)}"
        logger.error(msg)
        return {"error": msg}, 500


def create_user(data, files):
    """
    Create a new user with the given data.

    Args:
        data (dict): A dictionary containing user information.
        files (dict): A dictionary containing file data (profile picture).

    Returns:
        tuple: A response containing user data and an HTTP status code.
    """
    try:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        profile_picture = files.get('profile_picture')
        level = data.get('level', 1)
        experience_points = data.get('experience_points', 0)

        print("password:",password)
        if not password:
            raise ValueError("Password must be non-empty.")

        existing_user = UserDAL.get_user_by_email_or_username(email, username)
        if existing_user:
            msg = 'Email or username already exists.'
            logger.error(msg)
            return {'status': 'fail', 'message': msg}, 409

        user_role = UserDAL.get_role_by_name('Customer')
        if not user_role:
            msg = 'User role not found.'
            logger.error(msg)
            return {'status': 'fail', 'message': msg}, 500

        new_user = User(
            username=username,
            email=email,
            role_id=user_role.id,
            created_at=datetime.utcnow(),
            last_login=None
        )

        new_user.set_password(password)

        UserDAL.add_user(new_user)
        UserDAL.commit_changes()

        filename = 'default.jpg'
        if profile_picture and allowed_file(profile_picture.filename):
            filename = save_profile_picture(profile_picture)

        new_user_profile = UserProfile(
            user_id=new_user.id,
            profile_picture=filename,
            level=level,
            experience_points=experience_points
        )

        UserDAL.add_user_profile(new_user_profile)
        UserDAL.commit_changes()

        create_claims_for_user(
            user_id=new_user.id,
            username=username,
            email=email,
            role_name=user_role.name
        )

        logger.info('New user successfully created.')
        return {'status': 'success', 'message': 'Successfully created.', 'data': new_user.to_dict()}, 201

    except ValueError as e:
        logger.error(f'Error creating user: {str(e)}')
        return {'status': 'failed', 'message': str(e)}, 400

    except Exception as e:
        logger.error(f'Error creating user: {str(e)}')
        return {'status': 'failed', 'message': str(e)}, 500


def get_users():
    """
    Retrieve all users.

    Returns:
        tuple: A list of user data and an HTTP status code.
    """
    try:
        users = UserDAL.get_all_users()
        if not users:
            return [], 200
        users_list = [user.to_dict() for user in users]
        return users_list, 200
    except Exception as e:
        logger.error(f'Error fetching users: {str(e)}')
        return {'status': 'failed', 'message': str(e)}, 500


def get_user_by_id(user_id):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: The user data as a dictionary and an HTTP status code.
    """
    try:
        user = UserDAL.get_user_by_id(user_id)
        if not user:
            return None, 404
        return user.to_dict(), 200
    except Exception as e:
        logger.error(f'Error fetching user ID {user_id}: {str(e)}')
        return {'status': 'failed', 'message': str(e)}, 500


def update_user(user_id, data):
    """
    Update a user's details.

    Args:
        user_id (int): The ID of the user to update.
        data (dict): A dictionary containing user information to update.

    Returns:
        tuple: A response message and an HTTP status code.
    """
    try:
        email = data.get('email')
        password = data.get('password')

        user = UserDAL.get_user_by_id(user_id)

        if user is None:
            msg = f"User ID: {user_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        if email:
            existing_user_with_email = UserDAL.get_user_by_email(email)
            if existing_user_with_email and existing_user_with_email.id != user_id:
                msg = f"Email '{email}' already exists. Please choose a different email."
                logger.info(msg)
                return {'status': 'fail', 'message': msg}, 400

        password_hash = user.password_hash
        if password:
            user.set_password(password)
            password_hash = user.password_hash

        UserDAL.update_user(user, email=email, password_hash=password_hash)
        UserDAL.commit_changes()

        msg = f"User ID: {user_id} details updated successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 204

    except Exception as e:
        msg = f"Error updating user ID {user_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def delete_user(user_id):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        tuple: A response message and an HTTP status code.
    """
    try:
        user = UserDAL.get_user_by_id(user_id)
        if not user:
            return {'status': 'fail', 'message': f'User ID: {user_id} not found.'}, 404

        UserDAL.delete_user(user)
        UserDAL.commit_changes()

        return {'status': 'success', 'message': f'User ID: {user_id} deleted successfully.'}, 204

    except Exception as e:
        logger.error(f'Error deleting user ID {user_id}: {str(e)}')
        return {'status': 'failed', 'message': str(e)}, 500
