"""
Data Access Layer for managing Claim-related operations.

This module provides methods for accessing and manipulating claim
data in the database. It abstracts the details of database
interactions related to user claims.
"""

from app.models.claim import Claim, db
from sqlalchemy.exc import SQLAlchemyError


class ClaimDAL:
    """
    Class for accessing and manipulating Claim data.
    """
    @staticmethod
    def get_claims_by_user_id(user_id):
        """
        Retrieve all claims associated with a specific user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Claim objects for the specified user.
        """
        return Claim.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_claim(type, value, user_id):
        """
        Create a new claim for a user.

        Args:
            type (str): The type of the claim.
            value (str): The value of the claim.
            user_id (int): The ID of the user.

        Returns:
            Claim: The created Claim object.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            claim = Claim(type=type, value=value, user_id=user_id)
            db.session.add(claim)
            db.session.flush()
            return claim
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_claims_by_user_id(user_id):
        """
        Delete all claims associated with a specific user ID.

        Args:
            user_id (int): The ID of the user.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            Claim.query.filter_by(user_id=user_id).delete()
            db.session.commit()
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
