from app import db
from sqlalchemy_serializer import SerializerMixin


class UserProfile(db.Model, SerializerMixin):
    """
    UserProfile model to store additional user details.

    Attributes:
        id (int): Primary key, auto-increment.
        user_id (int): Foreign key referencing the User model.
        profile_picture (str): Path to the user's profile picture.
        level (int): User level, typically used in gamification.
        experience_points (int): Experience points earned by the user.
    """
    __tablename__ = 'user_profiles'
    serialize_only = ('id', 'user_id', 'level', 'experience_points', 'profile_picture')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_picture = db.Column(db.String(255), default='default.jpg')
    level = db.Column(db.Integer, default=1)
    experience_points = db.Column(db.Integer, default=0)
    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return f'<UserProfile id={self.id}, user_id={self.user_id}>'
