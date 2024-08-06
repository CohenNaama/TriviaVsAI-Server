from app.models.user import User, db
from app.models.role import Role
from sqlalchemy.exc import SQLAlchemyError


class UserDAL:
    @staticmethod
    def get_user_by_email(email):
        """Retrieve a user by their email address."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_email_or_username(email, username):
        """Retrieve a user by email or username."""
        return User.query.filter((User.email == email) | (User.username == username)).first()

    @staticmethod
    def get_role_by_name(role_name):
        """Retrieve a role by its name."""
        from app.models.role import Role
        return Role.query.filter_by(name=role_name).first()

    @staticmethod
    def add_user(user):
        """Add a new user to the database."""
        db.session.add(user)

    @staticmethod
    def add_user_profile(user_profile):
        """Add a new user profile to the database."""
        db.session.add(user_profile)

    @staticmethod
    def update_user(user, **kwargs):
        """Update user attributes."""
        for key, value in kwargs.items():
            setattr(user, key, value)

    @staticmethod
    def delete_user(user):
        """Delete a user from the database."""
        db.session.delete(user)

    @staticmethod
    def commit_changes():
        """Commit the current transaction."""
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve a user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        """Retrieve a user by their username."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all_users():
        """Retrieve all users."""
        return User.query.all()

    @staticmethod
    def add_claims(claims_list):
        try:
            for claim in claims_list:
                db.session.add(claim)
            db.session.flush()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
