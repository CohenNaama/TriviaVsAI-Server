from datetime import datetime
from app import db
from sqlalchemy_serializer import SerializerMixin


class Achievement(db.Model, SerializerMixin):
    """
    Achievement model to store user achievements.

    Attributes:
        id (int): Primary key, auto-increment.
        user_id (int): Foreign key referencing the User model.
        user (relationship): Relationship to the User model.
        achievement_name (str): Name of the achievement.
        description (str): Description of the achievement.
        date_awarded (datetime): Timestamp of when the achievement was awarded.
    """
    __tablename__ = 'achievements'
    serialize_only = ('id', 'user', 'user_id', 'achievement_name', 'description', 'date_awarded')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='achievements')
    achievement_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_awarded = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
              Convert the achievement instance to a dictionary.

              Returns:
                  dict: A dictionary representation of the achievement.
              """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'date_awarded': self.date_awarded,
            'achievement_name': self.achievement_name,
            'description': self.description,

        }

    def __repr__(self):
        return f"<Achievement id={self.id}, user={self.user.username}, name={self.achievement_name}>"
