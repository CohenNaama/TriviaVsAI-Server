"""
Service layer for managing category-related operations.

This module provides functions to handle the creation, retrieval, and deletion
of categories. It interacts with the Category Data Access Layer (DAL) to perform
database operations and manage category-related business logic.
"""

from app.dal.category_dal import CategoryDAL
from app.models.category import Category
from app.logging_config import logger


def create_category(data):
    """
    Create a new category.

    Args:
        data (dict): A dictionary containing category information.

    Returns:
        tuple: A response message and an HTTP status code.
    """
    category_name = data.get('name')
    if not category_name:
        msg = "Missing required field: name"
        logger.warn(msg)
        return {"message": msg}, 400

    try:
        existing_category = CategoryDAL.get_category_by_name(category_name)
        if existing_category:
            msg = f"Category '{category_name}' already exists."
            logger.info(msg)
            return {"message": msg}, 400

        category = Category(name=category_name)
        CategoryDAL.create_category(category)
        CategoryDAL.commit_changes()

        msg = f"Category '{category_name}' created successfully."
        logger.info(msg)
        return {"message": msg}, 201

    except Exception as e:
        msg = f"Error creating category '{category_name}': {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_all_categories():
    """
    Retrieve all categories.

    Returns:
        tuple: A list of categories and an HTTP status code.
    """
    try:
        categories = CategoryDAL.get_all_categories()
        if not categories:
            msg = "The categories list is empty!"
            logger.info(msg)
            return [], 200

        categories_list = [category.to_dict() for category in categories]
        return categories_list, 200

    except Exception as e:
        msg = f"Failed to return categories list! \nError: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_category_by_id(category_id):
    """
    Retrieve a category by its ID.

    Args:
        category_id (int): The ID of the category.

    Returns:
        tuple: A category object and an HTTP status code.
    """
    try:
        category = CategoryDAL.get_category_by_id(category_id)
        if not category:
            msg = f"Category with ID {category_id} not found."
            logger.info(msg)
            return {"message": msg}, 404

        return category.to_dict(), 200

    except Exception as e:
        msg = f"Error retrieving category by ID {category_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def update_category(category_id, data):
    """
    Update an existing category.

    Args:
        category_id (int): The ID of the category to update.
        data (dict): A dictionary containing updated category information.

    Returns:
        tuple: A response message and an HTTP status code.
    """
    try:
        category = CategoryDAL.get_category_by_id(category_id)
        if not category:
            msg = f"Category with ID {category_id} not found."
            logger.info(msg)
            return {"message": msg}, 404

        if 'name' in data:
            existing_category = CategoryDAL.get_category_by_name(data['name'])
            if existing_category and existing_category.id != category_id:
                msg = f"Category name '{data['name']}' already exists."
                logger.info(msg)
                return {"message": msg}, 400

        category.name = data.get('name', category.name)  # Update only the name
        CategoryDAL.commit_changes()

        msg = f"Category with ID {category_id} updated successfully."
        logger.info(msg)
        return {"message": msg}, 200

    except Exception as e:
        msg = f"Error updating category with ID {category_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def delete_category(category_id):
    """
    Delete a category.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        tuple: A response message and an HTTP status code.
    """
    try:
        category = CategoryDAL.get_category_by_id(category_id)
        if not category:
            msg = f"Category with ID {category_id} not found."
            logger.info(msg)
            return {"message": msg}, 404

        CategoryDAL.delete_category(category)
        CategoryDAL.commit_changes()

        msg = f"Category with ID {category_id} deleted successfully."
        logger.info(msg)
        return {"message": msg}, 200

    except Exception as e:
        msg = f"Error deleting category with ID {category_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500
