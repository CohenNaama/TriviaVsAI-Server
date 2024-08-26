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
from app.models.userProfile import db


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


# Experience point thresholds for different levels
LEVEL_THRESHOLDS = {
    1: 0,
    2: 50,
    3: 200,
    4: 500,
    5: 1000,
}


def map_level_to_category(level):
    """
    Maps a numerical level to a category string.

    Args:
        level (int): The player's level.

    Returns:
        str: The category corresponding to the player's level.
    """
    if level <= 3:
        return "new"
    elif 4 <= level <= 7:
        return "intermediate"
    else:
        return "advanced"


def calculate_player_level(experience_points):
    """
    Calculates the player's level based on their experience points.

    Args:
        experience_points (int): The total experience points of the player.

    Returns:
        int: The player's calculated level.
    """
    level = 1
    for lvl, xp_threshold in LEVEL_THRESHOLDS.items():
        if experience_points >= xp_threshold:
            level = lvl
        else:
            break
    return level


def update_player_level(user_profile):
    """
    Updates the player's level based on their current experience points.

    Args:
        user_profile (UserProfile): The user profile object containing the player's current level and experience points.
    """
    new_level = calculate_player_level(user_profile.experience_points)
    if user_profile.level != new_level:
        user_profile.level = new_level

        UserProfileDAL.commit_changes()


def award_experience_points(user_profile, points):
    """
    Awards experience points to the player and updates their level accordingly.

    Args:
        user_profile (UserProfile): The user profile object containing the player's current level and experience points.
        points (int): The number of experience points to be awarded to the player.
    """
    user_profile.experience_points += points
    update_player_level(user_profile)

    UserProfileDAL.commit_changes()
