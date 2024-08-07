"""
Route definitions for role-related endpoints.

This module defines the API endpoints for managing user roles, including
creating, retrieving, and listing roles. These routes leverage the service
layer to ensure proper request handling and business logic execution.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.role_service import create_role, get_all_roles, get_role_by_id
from app.middleware.decorators import admin_required, json_validator
from app.schemas.role_create_schema import create_role_schema

role_bp = Blueprint('role_bp', __name__)


@role_bp.route("/roles", methods=['POST'])
@jwt_required()
@admin_required()
@json_validator(create_role_schema)
def create_role_route():
    """
    Create a new role.

    Requires admin authentication.

    Returns:
        Response: JSON response with a status message and HTTP status code.
    """
    data = request.get_json()
    response, status = create_role(data)
    return jsonify(response), status


@role_bp.route("/roles", methods=['GET'])
@jwt_required()
@admin_required()
def get_all_roles_route():
    """
    Retrieve all roles.

    Requires admin authentication.

    Returns:
        Response: JSON response with a list of roles and HTTP status code.
    """
    response, status = get_all_roles()
    return jsonify(response), status


@role_bp.route("/roles/<int:role_id>", methods=['GET'])
@jwt_required()
@admin_required()
def get_role_by_id_route(role_id):
    """
    Retrieve a role by ID.

    Requires admin authentication.

    Args:
        role_id (int): ID of the role to retrieve.

    Returns:
        Response: JSON response with role data and HTTP status code.
    """
    response, status = get_role_by_id(role_id)
    return jsonify(response), status
