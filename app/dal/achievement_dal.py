"""
Data Access Layer for managing Achievement-related operations.

This module provides direct database interactions for achievement-related
actions, abstracting away the complexities of database operations
from the business logic in the service layer.
"""

from app.models.achievement import Achievement, db
from sqlalchemy.exc import SQLAlchemyError


class AchievementDAL:
    """
    Class for accessing and manipulating Achievement data.
    """

    @staticmethod
    def create_achievement(achievement_data):
        """
        Create a new achievement in the database.

        Args:
            achievement_data (dict): Data for creating a new achievement.

        Returns:
            Achievement: The created Achievement object.
        """
        try:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
            db.session.commit()
            return achievement
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_achievement_by_id(user_id, achievement_id):
        """
        Retrieve an achievement by its ID and user ID.

        Args:
            user_id (int): The ID of the user.
            achievement_id (int): The ID of the achievement.

        Returns:
            Achievement: The Achievement object with the specified ID and user ID.
        """
        return Achievement.query.filter_by(id=achievement_id, user_id=user_id).first()

    @staticmethod
    def get_all_achievements_of_user(user_id):
        """
        Retrieve all achievements of a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Achievement objects.
        """
        return Achievement.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_achievements():
        """
        Retrieve all achievements from the database.

        Returns:
            list: A list of Achievement objects.
        """
        return Achievement.query.all()

    @staticmethod
    def update_achievement(achievement_id, user_id, data):
        """
        Update an existing achievement in the database.

        Args:
            achievement_id (int): The ID of the achievement to update.
            user_id (int): The ID of the user who owns the achievement.
            data (dict): The new data for the achievement.

        Returns:
            Achievement: The updated Achievement object.
        """
        try:
            achievement = Achievement.query.filter_by(id=achievement_id, user_id=user_id).first()
            if not achievement:
                raise ValueError(f"Achievement with id {achievement_id} for user_id {user_id} not found.")

            achievement.achievement_name = data.get('achievement_name', achievement.achievement_name)
            achievement.description = data.get('description', achievement.description)
            achievement.date_awarded = data.get('date_awarded', achievement.date_awarded)
            db.session.commit()
            return achievement
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_achievement(achievement_id, user_id):
        """
        Delete an achievement from the database.

        Args:
            achievement_id (int): The ID of the achievement to delete.
            user_id (int): The ID of the user who owns the achievement.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            achievement = Achievement.query.filter_by(id=achievement_id, user_id=user_id).first()
            if not achievement:
                raise ValueError(f"Achievement with id {achievement_id} for user_id {user_id} not found.")

            db.session.delete(achievement)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
