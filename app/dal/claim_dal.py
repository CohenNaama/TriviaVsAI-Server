from app.models.claim import Claim, db
from sqlalchemy.exc import SQLAlchemyError


class ClaimDAL:
    @staticmethod
    def get_claims_by_user_id(user_id):
        return Claim.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_claim(type, value, user_id):
        try:
            claim = Claim(type=type, value=value, user_id=user_id)
            db.session.add(claim)
            db.session.flush()
            return claim
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_claims_by_user_id(user_id):
        try:
            Claim.query.filter_by(user_id=user_id).delete()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def commit_changes():
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
