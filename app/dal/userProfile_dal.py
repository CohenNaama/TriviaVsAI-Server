"""
Data Access Layer for managing UserProfile-related operations.

This module provides methods for accessing and manipulating user
profile data in the database, handling operations such as retrieval
and updates of user profiles.
"""

from app.models.userProfile import UserProfile, db
from sqlalchemy.exc import SQLAlchemyError


class UserProfileDAL:
    """
    Class for accessing and manipulating UserProfile data.
    """
    @staticmethod
    def get_all_profiles():
        """
        Retrieve all user profiles from the database.

        Returns:
            list: A list of UserProfile objects.
        """
        try:
            return UserProfile.query.all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_profile_by_user_id(user_id):
        """
        Retrieve a user profile by user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            UserProfile: The UserProfile object with the specified user ID.
        """
        try:
            return UserProfile.query.filter_by(user_id=user_id).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_user_profile(user_profile, profile_picture=None, level=None, experience_points=None):
        """
        Update user profile attributes.

        Args:
            user_profile (UserProfile): The UserProfile object to update.
            profile_picture (str, optional): The new profile picture filename.
            level (int, optional): The new user level.
            experience_points (int, optional): The new experience points.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            if profile_picture is not None:
                user_profile.profile_picture = profile_picture
            if level is not None:
                user_profile.level = level
            if experience_points is not None:
                user_profile.experience_points = experience_points
            db.session.flush()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def commit_changes():
        """
        Commit the current database transaction.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
