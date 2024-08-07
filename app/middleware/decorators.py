"""
Custom decorators for request handling and validation.

This module defines decorators for ensuring proper authentication,
authorization, and data validation on API endpoints.
"""

import jsonschema
from jsonschema import validate
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from flask import jsonify, request, abort, current_app
from functools import wraps
from app.logging_config import logger


def admin_required():
    """
    Decorator to ensure that the user has admin privileges.

    Returns:
        Response: JSON response with an error message if the user is not an admin.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:

                verify_jwt_in_request()
                claims = get_jwt()

                if claims['role'] and claims['role'] == 'Admin':
                    return fn(*args, **kwargs)

                else:
                    msg = 'Permission denied. Admins only!'
                    logger.log(level=40, msg=msg)
                    return jsonify(msg=msg), 403

            except Exception as e:
                logger.log(level=40, msg=f'Error in admin_required decorator: {str(e)}')
                return jsonify(msg="Internal Server Error"), 500

        return decorator

    return wrapper


def user_required():
    """
    Decorator to ensure that the user is authorized.

    Returns:
        Response: JSON response with an error message if the user is unauthorized.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                user_id_from_request = str(request.view_args.get('user_id'))

                if claims['user_id'] and claims['user_id'] == user_id_from_request:
                    # kwargs['user_id_from_request'] = user_id_from_request
                    return fn(*args, **kwargs)

                else:
                    msg = 'Permission denied. You are unauthorized to access!'
                    logger.log(level=40, msg=msg)
                    return jsonify(msg=msg), 403

            except Exception as e:
                logger.log(level=40, msg=f'Error in user_required decorator: {str(e)}')
                return jsonify(msg="Internal Server Error."), 500

        return decorator

    return wrapper


def permission_required():
    """
    Decorator to ensure that the user has the necessary permissions to access or modify resources.

    The user must either be an admin or the user associated with the request.

    Returns:
        Response: JSON response with an error message if the user lacks permissions.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                user_id_from_request = int(request.view_args.get('user_id'))

                if (claims['user_id'] and claims['user_id'] == str(user_id_from_request) or claims['role']
                        and claims['role'] == 'Admin'):
                    return fn(*args, **kwargs)
                else:
                    msg = "Permission denied. You can only update your own information or you must be an admin."
                    logger.log(level=40, msg=msg)
                    return jsonify(msg=msg), 403

            except Exception as e:
                logger.log(level=40, msg=f'Error in permission_required decorator: {str(e)}')
                return jsonify(msg="Internal Server Error"), 500

        return decorator

    return wrapper


def json_validator(schema):
    """
    Decorator to validate JSON request data against a schema.

    Args:
        schema (dict): The JSON schema to validate against.

    Returns:
        Response: JSON response with an error message if validation fails.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validate(request.json, schema)
            except jsonschema.ValidationError as e:
                msg = "Error: Invalid JSON data"
                logger.log(level=40, msg=msg)
                return jsonify({"message": msg, "details": e.message}), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator


def form_data_validator(schema):
    """
    Decorator to validate form data against a specified JSON schema.

    This decorator processes both form data and file uploads. It converts the form data
    into a dictionary and includes file information (if available) as part of the validation process.
    Specifically, it handles fields like 'level' and 'experience_points' by attempting to
    convert them into integers. It defaults the 'profile_picture' to 'default.jpg' if no file is uploaded.

    Args:
        schema (dict): The JSON schema to validate the form data against.

    Returns:
        Response: JSON response with an error message if validation fails, or
        calls the decorated function if validation is successful.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            form_data = request.form.to_dict()
            form_data['profile_picture'] = (
                request.files.get('profile_picture').filename
                if 'profile_picture' in request.files and request.files['profile_picture'].filename
                else 'default.jpg'
            )

            if 'level' in form_data:
                try:
                    form_data['level'] = int(form_data['level'])
                except (ValueError, TypeError):
                    form_data['level'] = None

            if 'experience_points' in form_data:
                try:
                    form_data['experience_points'] = int(form_data['experience_points'])
                except (ValueError, TypeError):
                    form_data['experience_points'] = None

            try:
                validate(form_data, schema)
            except jsonschema.ValidationError as e:
                msg = "Error: Invalid form data"
                logger.log(level=40, msg=msg)
                return jsonify({"message": msg, "details": e.message}), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator
