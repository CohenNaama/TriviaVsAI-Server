from datetime import datetime
from flask_bcrypt import Bcrypt
from app import db
from sqlalchemy_serializer import SerializerMixin

bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    """
       User model to store user details.

       Attributes:
        id (int): Primary key, auto-increment.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password for authentication.
        created_at (datetime): Timestamp of user creation.
        last_login (datetime): Timestamp of last user login.
        level (int): User level, typically used in gamification.
        experience_points (int): Experience points earned by the user.
        profile_picture (str): Path to the user's profile picture.
        role_id (int): Foreign key referencing Role.
        role (relationship): Relationship to Role model.

       """
    __tablename__ = 'users'
    serialize_only = ('id', 'username', 'email', 'role', 'created_at', 'last_login', 'level', 'experience_points',
                      'profile_picture')

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship("Role")
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    level = db.Column(db.Integer, default=1)
    experience_points = db.Column(db.Integer, default=0)
    profile_picture = db.Column(db.String(255), default='default.jpg')

    def set_password(self, password):
        """
              Set the user's password.

              Args:
                  password (str): Plain text password.
              """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
               Check the user's password.

               Args:
                   password (str): Plain text password.

               Returns:
                   bool: True if the password matches, False otherwise.
               """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: %r>' % self.username


    # def to_dict(self):
    #     """
    #           Convert the user object to a dictionary.
    #
    #           Returns:
    #               dict: Dictionary representation of the user.
    #           """
    #     user_dict = {
    #         'id': self.id,
    #         'username': self.username,
    #         'email': self.email,
    #         'role': self.role.to_dict() if self.role else None,
    #         'created_at': self.created_at,
    #         'last_login': self.last_login,
    #         'level': self.level,
    #         'experience_points': self.experience_points,
    #         'profile_picture': self.profile_picture,
    #     }
    #     return user_dict
