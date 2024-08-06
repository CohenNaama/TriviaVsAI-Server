from app.models.userProfile import UserProfile, db
from sqlalchemy.exc import SQLAlchemyError


class UserProfileDAL:
    @staticmethod
    def get_all_profiles():
        try:
            return UserProfile.query.all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_profile_by_user_id(user_id):
        try:
            return UserProfile.query.filter_by(user_id=user_id).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_user_profile(user_profile, profile_picture=None, level=None, experience_points=None):
        try:
            if profile_picture is not None:
                user_profile.profile_picture = profile_picture
            if level is not None:
                user_profile.level = level
            if experience_points is not None:
                user_profile.experience_points = experience_points
            db.session.flush()
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
