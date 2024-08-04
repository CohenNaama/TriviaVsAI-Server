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
    """
    __tablename__ = 'game_sessions'
    serialize_only = ('id', 'user', 'questions_asked', 'correct_answers', 'total_questions', 'start_time', 'end_time')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='game_sessions')
    questions_asked = db.Column(db.ARRAY(db.Integer), nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)

    def get_duration(self):
        """
        Calculate the duration of the game session.

        Returns:
            int: Duration of the session in seconds, or None if not completed.
        """
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds())
        return None

    def __repr__(self):
        return (f"<GameSession id={self.id}, user={self.user.username}, "
                f"correct_answers={self.correct_answers}, total_questions={self.total_questions}, "
                f"start_time={self.start_time}, end_time={self.end_time}>")
