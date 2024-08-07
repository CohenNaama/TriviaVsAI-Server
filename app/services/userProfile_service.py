"""
Service layer for managing user profile-related operations.

This module contains functions for handling the retrieval,
updating, and management of user profiles. It interacts with the
UserProfile Data Access Layer (DAL) to perform necessary database
operations.
"""

from app.dal.userProfile_dal import UserProfileDAL
from app.middleware.helpers import save_profile_picture
from app.logging_config import logger
from sqlalchemy.exc import SQLAlchemyError


def get_all_profiles():
    """
    Retrieve all user profiles.

    Returns:
        tuple: A list of user profile data and an HTTP status code.
    """
    try:
        users_profiles = UserProfileDAL.get_all_profiles()
        return [profile.to_dict() for profile in users_profiles], 200
    except Exception as e:
        msg = f'Failed to return users list! \nError: {str(e)}'
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_user_profile_by_id(user_id):
    """
    Retrieve a user profile by user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: The user profile data as a dictionary and an HTTP status code.
    """
    try:
        user_profile = UserProfileDAL.get_profile_by_user_id(user_id)
        if not user_profile:
            msg = f"User ID: {user_id} not found"
            logger.warn(msg)
            return None, {"message": msg}, 404

        return user_profile.to_dict(), 200
    except Exception as e:
        msg = f"Failed to return user ID: {user_id}. \nError: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def update_user_profile(user_id, form_data, files):
    """
    Update a user's profile.

    Args:
        user_id (int): The ID of the user whose profile is to be updated.
        form_data (dict): A dictionary containing profile fields to update.
        files (dict): A dictionary containing file data (profile picture).

    Returns:
        tuple: A response message and an HTTP status code.
    """
    try:
        user_profile = UserProfileDAL.get_profile_by_user_id(user_id)

        if user_profile is None:
            return {"status": "fail", "message": "User profile not found"}, 404

        profile_picture = files.get('profile_picture')
        level = form_data.get('level', type=int)
        experience_points = form_data.get('experience_points', type=int)

        if profile_picture:
            filename = save_profile_picture(profile_picture)
        else:
            filename = user_profile.profile_picture

        UserProfileDAL.update_user_profile(
            user_profile=user_profile,
            profile_picture=filename,
            level=level,
            experience_points=experience_points
        )

        UserProfileDAL.commit_changes()

        msg = f"User ID: {user_id} details updated successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 204

    except SQLAlchemyError as e:
        msg = f"Database error during user update: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500

    except Exception as e:
        msg = f"An unexpected error occurred during user update: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500
