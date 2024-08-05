import jsonschema
from jsonschema import validate
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from flask import jsonify, request, abort, current_app
from functools import wraps
from app.logging_config import logger


def admin_required():
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


def multipart_validator(required_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_fields = [field for field in required_fields if field not in request.form and field not in request.files]
            if missing_fields:
                msg = f"Missing fields: {', '.join(missing_fields)}"
                logger.error(msg)
                return jsonify({"message": msg}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator
