"""
Data Access Layer for managing role-related operations.

This module provides methods for accessing and manipulating role
data in the database, handling CRUD operations related to user roles.
"""

from app.models.role import Role, db
from sqlalchemy.exc import SQLAlchemyError


class RoleDAL:
    """
    Class for accessing and manipulating Role data.
    """
    @staticmethod
    def get_all_roles():
        """
        Retrieve all roles from the database.

        Returns:
            list: A list of Role objects.
        """
        return Role.query.all()

    @staticmethod
    def get_role_by_id(role_id):
        """
        Retrieve a role by its ID.

        Args:
            role_id (int): The ID of the role.

        Returns:
            Role: The Role object with the specified ID.
        """
        return Role.query.get(role_id)

    @staticmethod
    def get_role_by_name(name):
        """
        Retrieve a role by its name.

        Args:
            name (str): The name of the role.

        Returns:
            Role: The Role object with the specified name.
        """
        return Role.query.filter_by(name=name).first()

    @staticmethod
    def create_role(role):
        """
        Create a new role in the database.

        Args:
            role (Role): The Role object to add.

        Returns:
            Role: The created Role object.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            db.session.add(role)
            db.session.flush()
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_role(role):
        """
        Delete a role from the database.

        Args:
            role (Role): The Role object to delete.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            db.session.delete(role)
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
