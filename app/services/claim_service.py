from app.models.claim import Claim, db


def create_claims_for_user(user_id, username, email, role_name):
    claims_list = [
        {'type': 'user_id', 'value': str(user_id), 'user_id': user_id},
        {'type': 'username', 'value': username, 'user_id': user_id},
        {'type': 'email', 'value': email, 'user_id': user_id},
        {'type': 'role', 'value': role_name, 'user_id': user_id},
    ]
    for item in claims_list:
        claim = Claim(type=item['type'], value=item['value'], user_id=item['user_id'])
        db.session.add(claim)
    db.session.flush()
