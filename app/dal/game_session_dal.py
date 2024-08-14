"""
Data Access Layer for managing GameSession-related operations.

This module provides direct database interactions for game session-related
actions, abstracting away the complexities of database operations
from the business logic in the service layer.
"""

from app.models.gameSession import GameSession, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class GameSessionDAL:
    """
    Class for accessing and manipulating GameSession data.
    """

    @staticmethod
    def create_game_session(session_data):
        """
        Create a new game session in the database.

        Args:
            session_data (dict): Data for creating a new game session.

        Returns:
            GameSession: The created GameSession object.
        """
        try:
            session = GameSession(**session_data)
            db.session.add(session)
            db.session.commit()
            return session
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_game_session_by_id(user_id, session_id):
        """
        Retrieve a game session by its ID and user ID.

        Args:
            user_id (int): The ID of the user.
            session_id (int): The ID of the game session.

        Returns:
            GameSession: The GameSession object with the specified ID and user ID.
        """
        return GameSession.query.filter_by(id=session_id, user_id=user_id).first()

    @staticmethod
    def get_all_game_sessions_of_user(user_id):
        """
        Retrieve all game sessions of a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of GameSession objects.
        """
        return GameSession.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_game_sessions():
        """
        Retrieve all game sessions from the database.

        Returns:
            list: A list of GameSession objects.
        """
        return GameSession.query.all()

    @staticmethod
    def update_game_session(session_id, user_id, data):
        """
        Update an existing game session in the database.

        Args:
            session_id (int): The ID of the game session to update.
            user_id (int): The ID of the user who owns the game session.
            data (dict): The new data for the game session.

        Returns:
            GameSession: The updated GameSession object.
        """
        try:
            session = GameSession.query.filter_by(id=session_id, user_id=user_id).first()
            if not session:
                raise ValueError(f"GameSession with id {session_id} for user_id {user_id} not found.")

            # Update the fields if they are present in the data dictionary
            for key, value in data.items():
                if hasattr(session, key):
                    setattr(session, key, value)

            db.session.commit()
            return session
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_game_session(session_id, user_id):
        """
        Delete a game session from the database.

        Args:
            session_id (int): The ID of the game session to delete.
            user_id (int): The ID of the user who owns the game session.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            session = GameSession.query.filter_by(id=session_id, user_id=user_id).first()
            if not session:
                raise ValueError(f"GameSession with id {session_id} for user_id {user_id} not found.")

            db.session.delete(session)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_most_recent_session(user_id):
        """
        Retrieve the most recent game session for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            GameSession: The most recent GameSession object.
        """
        return GameSession.query.filter_by(user_id=user_id).order_by(GameSession.start_time.desc()).first()

    @staticmethod
    def finalize_session(session):
        """
        Finalize the game session by marking it as inactive and saving the end time.
        Args:
            session (GameSession): The GameSession object to finalize.
        """
        try:
            session.is_active = False
            session.is_finalized = True
            session.end_time = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def commit_changes():
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
