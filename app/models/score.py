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
    serialize_only = ('id', 'user', 'score', 'date', 'category', 'duration')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='scores')
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref='scores')
    duration = db.Column(db.Integer)

    def __repr__(self):
        return f"<Score id={self.id}, user={self.user.username}, score={self.score}, date={self.date}>"
