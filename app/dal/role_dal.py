from app.models.role import Role, db
from sqlalchemy.exc import SQLAlchemyError


class RoleDAL:
    @staticmethod
    def get_all_roles():
        return Role.query.all()

    @staticmethod
    def get_role_by_id(role_id):
        return Role.query.get(role_id)

    @staticmethod
    def get_role_by_name(name):
        return Role.query.filter_by(name=name).first()

    @staticmethod
    def create_role(role):
        try:
            db.session.add(role)
            db.session.flush()
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_role(role):
        try:
            db.session.delete(role)
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
