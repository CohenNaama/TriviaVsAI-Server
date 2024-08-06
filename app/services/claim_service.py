from app.dal.claim_dal import ClaimDAL
from app.logging_config import logger


def create_claims_for_user(user_id, username, email, role_name):
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
