"""
Data Access Layer for managing Question-related operations.

This module provides direct database interactions for question-related
actions, abstracting away the complexities of database operations
from the business logic in the service layer.
"""

from app.models.question import Question, db
from sqlalchemy.exc import SQLAlchemyError


class QuestionDAL:
    """
    Class for accessing and manipulating Question data.
    """

    @staticmethod
    def create_question(question_data):
        """
        Create a new question in the database.

        Args:
            question_data (dict): Data for creating a new question.

        Returns:
            Question: The created Question object.
        """
        try:
            question = Question(**question_data)
            db.session.add(question)
            db.session.flush()
            return question
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def is_duplicate_question(question_text):
        """
        Check if a question with the same text already exists.

        Args:
            question_text (str): The text of the question to check.

        Returns:
            bool: True if the question is a duplicate, False otherwise.
        """
        existing_question = Question.query.filter_by(question_text=question_text).first()
        return existing_question is not None

    @staticmethod
    def get_question_by_id(question_id):
        """
        Retrieve a question by its ID.

        Args:
            question_id (int): The ID of the question.

        Returns:
            Question: The Question object with the specified ID.
        """
        return Question.query.get(question_id)

    @staticmethod
    def get_all_questions():
        """
        Retrieve all questions from the database.

        Returns:
            list: A list of Question objects.
        """
        return Question.query.all()

    @staticmethod
    def update_question(question, **kwargs):
        """
        Update a question's attributes.

        Args:
            question (Question): The question to update.
            **kwargs: The attributes to update.
        """
        try:
            for key, value in kwargs.items():
                setattr(question, key, value)
            db.session.flush()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_question(question):
        """
        Delete a question from the database.

        Args:
            question (Question): The question to delete.
        """
        try:
            db.session.delete(question)
            db.session.commit()
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
