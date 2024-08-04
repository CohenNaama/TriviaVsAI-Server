from datetime import datetime
import enum
from app import db
from sqlalchemy_serializer import SerializerMixin


class DifficultyLevel(enum.Enum):
    """
    Enum to represent the difficulty levels of questions.

    Attributes:
        EASY: Represents an easy difficulty level.
        MEDIUM: Represents a medium difficulty level.
        HARD: Represents a hard difficulty level.
    """
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


class Question(db.Model, SerializerMixin):
    """
    Question model to store trivia questions.

    Attributes:
        id (int): Primary key, auto-increment.
        category_id (int): Foreign key referencing the Category.
        category (relationship): Relationship to the Category model.
        difficulty (enum): Difficulty level of the question.
        question_text (str): Text of the question.
        answer (str): Correct answer to the question.
        incorrect_answers (list): List of incorrect answers.
        created_at (datetime): Timestamp of when the question was created.
        times_asked (int): Number of times the question has been asked.
        success_rate (float): Rate of correct answers for this question.
    """
    __tablename__ = 'questions'
    serialize_only = ('id', 'category', 'difficulty', 'question_text', 'answer',
                      'incorrect_answers', 'created_at', 'times_asked', 'success_rate')

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  # Use 'categories.id'
    category = db.relationship('Category', backref='questions')
    difficulty = db.Column(db.Enum(DifficultyLevel), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    incorrect_answers = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    times_asked = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Question id={self.id}, category={self.category.name}, difficulty={self.difficulty.name}>"

    # def update_success_rate(self, correct_count, total_count):
    #     """
    #     Update the success rate of the question.
    #
    #     Args:
    #         correct_count (int): Number of correct answers.
    #         total_count (int): Total number of times the question was asked.
    #     """
    #     if total_count > 0:
    #         self.success_rate = correct_count / total_count
    #     else:
    #         self.success_rate = 0.0
