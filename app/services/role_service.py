from flask import Blueprint, request, jsonify
from app.models.role import Role, db
from app.middleware.jwt_decorators import admin_required, json_validator
from app. middleware.helpers import create_role_schema
from flask_jwt_extended import jwt_required
from app.logging_config import logger

role_service_bp = Blueprint('role_service', __name__)


@role_service_bp.route("/roles", methods=['POST'])
@jwt_required()
@admin_required()
@json_validator(create_role_schema)
def create_role():
    try:
        body = request.get_json()
        role_name = body.get('role_name', None)
        if role_name is None:
            msg = "missing required field: role_name"
            logger.warn(msg)
            return jsonify({"Message": msg}), 400

        existing_role = Role.query.filter_by(name=role_name).first()

        if existing_role:
            msg = f"Role '{role_name}' already exists."
            logger.info(msg)
            return jsonify({"message": msg})

        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()
        msg = f"Role '{role_name}' created successfully."
        logger.info(msg)

        return jsonify({"message": msg}), 201

    except Exception as e:
        msg = f"Error creating role '{role_name}': {str(e)}"
        logger.error(msg)
        db.session.rollback()
        return jsonify({
            'status': 'failed',
            'message': msg
        }), 500


@role_service_bp.route("/roles", methods=['GET'])
@jwt_required()
@admin_required()
def get_all_roles():
    try:
        roles = Role.query.all()
        if not roles:
            msg = "The roles list is empty!"
            logger.info(msg)
            return jsonify([], {'message': msg}), 200

        roles_list = [role.to_dict() for role in roles]
        return jsonify("Roles list:", roles_list), 200

    except Exception as e:
        msg = f"Failed to return roles list! \nError: {str(e)}"
        logger.error(msg)
        return jsonify({
            'status': 'failed',
            'message': msg,
        }), 500


@role_service_bp.route("/roles/<int:role_id>", methods=['GET'])
@jwt_required()
@admin_required()
def get_role_by_id(role_id):
    try:
        role = Role.query.filter_by(id=role_id).first()
        if role:
            return role.to_dict(), 200
        else:
            msg = f"Role {role_id} doesn't exists."
            logger.warn(msg)
            return jsonify(None, {"message": msg}), 404,

    except Exception as e:
        msg = f"Error while receiving the role: {str(e)}"
        logger.error(msg)
        return jsonify({
            'status': 'failed',
            'message': msg,
        }), 500
