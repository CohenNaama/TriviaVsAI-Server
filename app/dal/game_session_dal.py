"""
Data Access Layer for managing GameSession-related operations.

This module provides direct database interactions for game session-related
actions, abstracting away the complexities of database operations
from the business logic in the service layer.
"""

from app.models.gameSession import GameSession, db
from sqlalchemy.exc import SQLAlchemyError


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

            session.questions_asked = data.get('questions_asked', session.questions_asked)
            session.correct_answers = data.get('correct_answers', session.correct_answers)
            session.total_questions = data.get('total_questions', session.total_questions)
            session.start_time = data.get('start_time', session.start_time)
            session.end_time = data.get('end_time', session.end_time)
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
