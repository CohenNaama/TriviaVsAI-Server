"""
Service layer for managing user claim-related operations.

This module provides functionality for handling the creation of user claims.
It uses the Claims Data Access Layer (DAL) to interact with the database
and maintain claim-related business logic.
"""

from app.dal.claim_dal import ClaimDAL
from app.logging_config import logger


def create_claims_for_user(user_id, username, email, role_name):
    """
    Create claims for a user based on their ID, username, email, and role.

    Args:
        user_id (int): The ID of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        role_name (str): The role name of the user.

    Raises:
        Exception: If an error occurs while creating claims.
    """
    claims_list = [
        {'type': 'user_id', 'value': str(user_id)},
        {'type': 'username', 'value': username},
        {'type': 'email', 'value': email},
        {'type': 'role', 'value': role_name},
    ]

    try:
        for item in claims_list:
            ClaimDAL.create_claim(type=item['type'], value=item['value'], user_id=user_id)

        ClaimDAL.commit_changes()
        logger.info(f"Claims for user ID {user_id} created successfully.")
    except Exception as e:
        msg = f"Error creating claims for user ID {user_id}: {str(e)}"
        logger.error(msg)
        raise e  
