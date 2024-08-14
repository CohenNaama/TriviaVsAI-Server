from datetime import datetime
from app import db
from sqlalchemy_serializer import SerializerMixin


class GameSession(db.Model, SerializerMixin):
    """
    GameSession model to track individual game sessions for users.

    Attributes:
        id (int): Primary key, auto-increment.
        user_id (int): Foreign key referencing the User model.
        user (relationship): Relationship to the User model.
        questions_asked (list): List of question IDs asked during the session.
        correct_answers (int): Number of correct answers given by the user.
        total_questions (int): Total number of questions asked in the session.
        start_time (datetime): Timestamp when the session started.
        end_time (datetime): Timestamp when the session ended.
        is_active (bool): Whether the session is still ongoing.
        is_finalized (bool): Whether the session is completed and locked.
        skill_levels (dict): Tracks performance by category, mapping category IDs
                             to the number of correct answers and total attempts during the session.

    """
    __tablename__ = 'game_sessions'
    serialize_only = ('id', 'user', 'questions_asked', 'correct_answers', 'total_questions', 'start_time', 'end_time')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('game_sessions', cascade='all, delete-orphan'))
    questions_asked = db.Column(db.ARRAY(db.Integer), nullable=False, default=[])
    correct_answers = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_finalized = db.Column(db.Boolean, default=False)
    skill_levels = db.Column(db.JSON, default={})

    def get_duration(self):
        """
        Calculate the duration of the game session.

        Returns:
            int: Duration of the session in seconds, or None if not completed.
        """
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds())
        return None

    def to_dict(self):
        """
        Convert the game session instance to a dictionary.

        Returns:
            dict: A dictionary representation of the game session.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'questions_asked': self.questions_asked,
            'correct_answers': self.correct_answers,
            'total_questions': self.total_questions,
            'duration': self.get_duration(),
            'is_active': self.is_active,
            'is_finalized': self.is_finalized,
            'skill_levels': self.skill_levels

        }

    def __repr__(self):
        return (f"<GameSession id={self.id}, user={self.user.username}, "
                f"correct_answers={self.correct_answers}, total_questions={self.total_questions}, "
                f"start_time={self.start_time}, end_time={self.end_time}>")
