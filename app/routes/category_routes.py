"""
Route definitions for category-related endpoints.

This module defines the API endpoints for managing question categories,
including creating, retrieving, listing, and deleting categories. These routes
leverage the service layer to ensure proper request handling and business logic execution.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.category_service import (create_category, get_all_categories, get_category_by_id, update_category,
                                           delete_category)
from app.middleware.decorators import admin_required, json_validator
from app.schemas.category_schemas import category_create_schema

category_bp = Blueprint('category_bp', __name__)


@category_bp.route("/categories", methods=['POST'])
@jwt_required()
@admin_required()
@json_validator(category_create_schema)
def create_category_route():
    """
    Create a new category.

    Requires admin authentication.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    data = request.get_json()
    response, status = create_category(data)
    return jsonify(response), status


@category_bp.route("/categories", methods=['GET'])
@jwt_required()
@admin_required()
def get_all_categories_route():
    """
    Retrieve all categories.

    Requires admin authentication.

    Returns:
        Response: JSON response with a list of categories and HTTP status code.
    """
    response, status = get_all_categories()
    return jsonify(response), status


@category_bp.route("/categories/<int:category_id>", methods=['GET'])
@jwt_required()
@admin_required()
def get_category_by_id_route(category_id):
    """
    Retrieve a category by its ID.

    Requires admin authentication.

    Args:
        category_id (int): The ID of the category.

    Returns:
        Response: JSON response with a category and HTTP status code.
    """
    response, status = get_category_by_id(category_id)
    return jsonify(response), status


@category_bp.route("/categories/<int:category_id>", methods=['PUT'])
@jwt_required()
@admin_required()
@json_validator(category_create_schema)
def update_category_route(category_id):
    """
    Update a category.

    Requires admin authentication.

    Args:
        category_id (int): The ID of the category to update.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    data = request.get_json()
    response, status = update_category(category_id, data)
    return jsonify(response), status


@category_bp.route("/categories/<int:category_id>", methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_category_route(category_id):
    """
    Delete a category.

    Requires admin authentication.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    response, status = delete_category(category_id)
    return jsonify(response), status
