from app.services.user_service import login as login_service
from flask_jwt_extended import jwt_required
from app.middleware.jwt_decorators import json_validator, permission_required, form_data_validator
from app.schemas.user_schema import login_schema, user_create_schema, user_update_schema
from flask import Blueprint, request, jsonify
from app.services.user_service import (
    create_user as create_user_service,
    get_users as get_users_service,
    get_user_by_id as get_user_by_id_service,
    update_user as update_user_service,
    delete_user as delete_user_service
)


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
@json_validator(login_schema)
def login():
    data = request.json
    response, status = login_service(data)
    return jsonify(response), status


@user_bp.route('/users', methods=['POST'])
@form_data_validator(user_create_schema)
def create_user():
    data = request.form.to_dict()
    files = request.files
    response, status = create_user_service(data, files)
    return jsonify(response), status


@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    response, status = get_users_service()
    return jsonify(response), status


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    response, status = get_user_by_id_service(user_id)
    return jsonify(response), status


@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
@permission_required()
@json_validator(user_update_schema)
def update_user(user_id):
    data = request.json
    response, status = update_user_service(user_id, data)
    return jsonify(response), status


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@permission_required()
def delete_user(user_id):
    response, status = delete_user_service(user_id)
    return jsonify(response), status
