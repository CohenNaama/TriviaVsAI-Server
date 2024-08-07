"""
Data Access Layer for managing category-related operations.

This module provides methods for accessing and manipulating category
data in the database, handling CRUD operations related to question categories.
"""

from app.models.category import Category, db
from sqlalchemy.exc import SQLAlchemyError


class CategoryDAL:
    """
    Class for accessing and manipulating Category data.
    """
    @staticmethod
    def get_all_categories():
        """
        Retrieve all categories from the database.

        Returns:
            list: A list of Category objects.
        """
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        """
        Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            Category: The Category object, or None if not found.
        """
        return Category.query.get(category_id)

    @staticmethod
    def get_category_by_name(category_name):
        """
        Retrieve a category by its name.

        Args:
            category_name (str): The name of the category to retrieve.

        Returns:
            Category: The Category object, or None if not found.
        """
        return Category.query.filter_by(name=category_name).first()

    @staticmethod
    def create_category(category):
        """
        Add a new category to the database.

        Args:
            category (Category): The Category object to add.
        """
        db.session.add(category)

    @staticmethod
    def update_category(category, data):
        """
        Update a category in the database.

        Args:
            category (Category): The Category object to update.
            data (dict): A dictionary containing updated category information.
        """
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)

    @staticmethod
    def delete_category(category):
        """
        Delete a category from the database.

        Args:
            category (Category): The Category object to delete.
        """
        db.session.delete(category)

    @staticmethod
    def commit_changes():
        """
        Commit changes to the database.
        """
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
