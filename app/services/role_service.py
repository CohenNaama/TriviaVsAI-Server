from app.dal.role_dal import RoleDAL
from app.models.role import Role
from app.logging_config import logger


def create_role(data):
    """Create a new role."""
    role_name = data.get('role_name')
    if not role_name:
        msg = "Missing required field: role_name"
        logger.warn(msg)
        return {"message": msg}, 400

    try:
        existing_role = RoleDAL.get_role_by_name(role_name)
        if existing_role:
            msg = f"Role '{role_name}' already exists."
            logger.info(msg)
            return {"message": msg}, 400

        role = Role(name=role_name)
        RoleDAL.create_role(role)
        RoleDAL.commit_changes()

        msg = f"Role '{role_name}' created successfully."
        logger.info(msg)
        return {"message": msg}, 201

    except Exception as e:
        msg = f"Error creating role '{role_name}': {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_all_roles():
    """Retrieve all roles."""
    try:
        roles = RoleDAL.get_all_roles()
        if not roles:
            msg = "The roles list is empty!"
            logger.info(msg)
            return [], 200

        roles_list = [role.to_dict() for role in roles]
        return roles_list, 200

    except Exception as e:
        msg = f"Failed to return roles list! \nError: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_role_by_id(role_id):
    """Retrieve a role by ID."""
    try:
        role = RoleDAL.get_role_by_id(role_id)
        if role:
            return role.to_dict(), 200
        else:
            msg = f"Role {role_id} doesn't exist."
            logger.warn(msg)
            return None, 404

    except Exception as e:
        msg = f"Error while receiving the role: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500
