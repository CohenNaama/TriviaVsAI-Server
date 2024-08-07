"""
Data Access Layer for managing User-related operations.

This module provides direct database interactions for user-related
actions, abstracting away the complexities of database operations
from the business logic in the service layer.
"""

from app.models.user import User, db
from app.models.role import Role


class UserDAL:
    """
    Class for accessing and manipulating User data.
    """

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The User object with the specified email.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_email_or_username(email, username):
        """
        Retrieve a user by email or username.

        Args:
            email (str): The email address of the user.
            username (str): The username of the user.

        Returns:
            User: The User object with the specified email or username.
        """
        return User.query.filter((User.email == email) | (User.username == username)).first()

    @staticmethod
    def get_role_by_name(role_name):
        """
        Retrieve a role by its name.

        Args:
            role_name (str): The name of the role.

        Returns:
            Role: The Role object with the specified name.
        """
        from app.models.role import Role
        return Role.query.filter_by(name=role_name).first()

    @staticmethod
    def add_user(user):
        """
        Add a new user to the database.

        Args:
            user (User): The User object to add.
        """
        db.session.add(user)

    @staticmethod
    def add_user_profile(user_profile):
        """
        Add a new user profile to the database.

        Args:
            user_profile (UserProfile): The UserProfile object to add.
        """
        db.session.add(user_profile)

    @staticmethod
    def update_user(user, **kwargs):
        """
        Update user attributes.

        Args:
            user (User): The User object to update.
            kwargs (dict): The attributes to update and their new values.
        """
        for key, value in kwargs.items():
            setattr(user, key, value)

    @staticmethod
    def delete_user(user):
        """
        Delete a user from the database.

        Args:
            user (User): The User object to delete.
        """
        db.session.delete(user)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The User object with the specified ID.
        """
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The User object with the specified username.
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all_users():
        """
        Retrieve all users.

        Returns:
            list: A list of User objects.
        """
        return User.query.all()

    @staticmethod
    def commit_changes():
        """
        Commit the current database transaction.

        Raises:
            SQLAlchemyError: If there is an error during the database operation.
        """
        db.session.commit()
