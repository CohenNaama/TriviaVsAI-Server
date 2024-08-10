"""
Service layer for managing achievement-related operations.

This module provides functions to handle the creation, retrieval, and deletion
of achievements. It interacts with the Achievement Data Access Layer (DAL) to perform
database operations and manage achievement-related business logic.
"""

from app.dal.achievement_dal import AchievementDAL


def create_achievement_service(achievement_data):
    """
    Service function to create a new achievement.

    Args:
        achievement_data (dict): Data for creating a new achievement.

    Returns:
        dict: Response message and status code.
    """
    try:
        achievement = AchievementDAL.create_achievement(achievement_data)
        return {'status': 'success',
                'message': 'Achievement created successfully.',
                'data': achievement.to_dict()}, 201
    except Exception as e:
        return {'status': 'failed', 'message': f"Error creating achievement: {str(e)}"}, 500


def get_achievement_service(user_id, achievement_id):
    """
    Service function to retrieve an achievement by its ID and user ID.

    Args:
        user_id (int): The ID of the user.
        achievement_id (int): The ID of the achievement.

    Returns:
        dict: Response message and status code.
    """
    try:
        achievement = AchievementDAL.get_achievement_by_id(user_id, achievement_id)
        if not achievement:
            return {'status': 'failed', 'message': 'Achievement not found.'}, 404
        return {'status': 'success', 'data': achievement.to_dict()}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving achievement: {str(e)}"}, 500


def get_all_achievements_of_user_service(user_id):
    """
    Service function to retrieve all achievements of a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Response message and status code.
    """
    try:
        achievements = AchievementDAL.get_all_achievements_of_user(user_id)
        return {'status': 'success', 'data': [achievement.to_dict() for achievement in achievements]}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving achievements: {str(e)}"}, 500


def get_all_achievements_service():
    """
    Service function to retrieve all achievements.

    Returns:
        dict: Response message and status code.
    """
    try:
        achievements = AchievementDAL.get_all_achievements()
        return {'status': 'success', 'data': [achievement.to_dict() for achievement in achievements]}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving achievements: {str(e)}"}, 500


def update_achievement_service(achievement_id, user_id, data):
    """
    Service function to update an achievement.

    Args:
        achievement_id (int): The ID of the achievement to update.
        user_id (int): The ID of the user who owns the achievement.
        data (dict): The new data for the achievement.

    Returns:
        dict: Response message and status code.
    """
    try:
        updated_achievement = AchievementDAL.update_achievement(achievement_id, user_id, data)
        return {'status': 'success', 'message': 'Achievement updated successfully.', 'data': updated_achievement.to_dict()}, 204
    except Exception as e:
        return {'status': 'failed', 'message': f"Error updating achievement: {str(e)}"}, 500


def delete_achievement_service(user_id, achievement_id):
    """
    Service function to delete an achievement.

    Args:
        user_id (int): The ID of the user who owns the achievement.
        achievement_id (int): The ID of the achievement to delete.

    Returns:
        dict: Response message and status code.
    """
    try:
        result = AchievementDAL.delete_achievement(achievement_id, user_id)
        if not result:
            return {'status': 'failed', 'message': 'Achievement not found.'}, 404
        return {'status': 'success', 'message': 'Achievement deleted successfully.'}, 204
    except Exception as e:
        return {'status': 'failed', 'message': f"Error deleting achievement: {str(e)}"}, 500
