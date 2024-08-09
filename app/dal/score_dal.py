"""
Data Access Layer for managing Score-related operations.

This module provides direct database interactions for score-related
actions, abstracting away the complexities of database operations
from the business logic in the service layer.
"""

from app.models.score import Score, db
from sqlalchemy.exc import SQLAlchemyError


class ScoreDAL:
    """
    Class for accessing and manipulating Score data.
    """

    @staticmethod
    def create_score(score_data):
        """
        Create a new score in the database.

        Args:
            score_data (dict): Data for creating a new score.

        Returns:
            Score: The created Score object.
        """
        try:
            score = Score(**score_data)
            db.session.add(score)
            db.session.commit()
            return score
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_score_by_id(user_id, score_id):
        """
        Retrieve a score by its ID and user ID.

        Args:
            user_id (int): The ID of the user.
            score_id (int): The ID of the score.

        Returns:
            Score: The Score object with the specified ID and user ID.
        """
        return Score.query.filter_by(id=score_id, user_id=user_id).first()

    @staticmethod
    def get_all_scores_of_user(user_id):
        """
        Retrieve all scores of user from the database.

        Returns:
            list: A list of Score objects.
        """
        return Score.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_scores():
        """
        Retrieve all scores from the database.

        Returns:
            list: A list of Score objects.
        """
        return Score.query.all()

    @staticmethod
    def update_score(score_id, user_id, data):
        """
        Update an existing score in the database.

        Args:
            score_id (int): The ID of the score to update.
            user_id (int): The ID of the user who owns the score.
            data (dict): The new data for the score.

        Returns:
            Score: The updated Score object.
        """
        try:
            score = Score.query.filter_by(id=score_id, user_id=user_id).first()
            if not score:
                raise ValueError(f"Score with id {score_id} for user_id {user_id} not found.")

            score.score = data.get('score', score.score)
            score.category_id = data.get('category_id', score.category_id)
            score.duration = data.get('duration', score.duration)
            db.session.commit()
            return score
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_score(score_id, user_id):
        """
        Delete a score from the database.

        Args:
            score_id (int): The ID of the score to delete.
            user_id (int): The ID of the user who owns the score.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            score = Score.query.filter_by(id=score_id, user_id=user_id).first()
            if not score:
                raise ValueError(f"Score with id {score_id} for user_id {user_id} not found.")

            db.session.delete(score)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def commit_changes():
        """
        Commit the current transaction.
        """
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
