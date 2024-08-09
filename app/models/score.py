from datetime import datetime
from app import db
from sqlalchemy_serializer import SerializerMixin


class Score(db.Model, SerializerMixin):
    """
    Score model to store user scores for game sessions.

    Attributes:
        id (int): Primary key, auto-increment.
        user_id (int): Foreign key referencing the User model.
        user (relationship): Relationship to the User model.
        score (int): The score achieved by the user.
        date (datetime): Timestamp of when the score was recorded.
        category_id (int): Foreign key referencing the Category model.
        category (relationship): Relationship to the Category model.
        duration (int): Duration in seconds of the game session.
    """
    __tablename__ = 'scores'
    serialize_only = ('id', 'user_id', 'user', 'score', 'date', 'category_id', 'duration')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='scores')
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref='scores')
    duration = db.Column(db.Integer)

    def to_dict(self):
        """
              Convert the score instance to a dictionary.

              Returns:
                  dict: A dictionary representation of the score.
              """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'date': self.date,
            'score': self.score,
            'category_id': self.category_id,
            'duration': self.duration,
        }

    def __repr__(self):
        return f"<Score id={self.id}, user={self.user.username}, score={self.score}, date={self.date}>"
