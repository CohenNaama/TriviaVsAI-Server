from app.helpers.feedback_helper import decrease_difficulty, increase_difficulty
from app.models.gameSession import GameSession
from app.models.question import DifficultyLevel


def adjust_difficulty(user_id, streak, current_difficulty):
    """
    Adjust the difficulty of the next question based on the user's performance,
    considering both streaks and overall accuracy.

    Args:
        user_id (int): The ID of the user.
        streak (dict): The player's current streaks, including 'correct_streak' and 'incorrect_streak'.
        current_difficulty (str): The current difficulty level of questions.

    Returns:
        str: The adjusted difficulty level.
    """
    if streak['correct_streak'] >= 5:
        return increase_difficulty(current_difficulty)
    elif streak['incorrect_streak'] >= 3:
        return decrease_difficulty(current_difficulty)

    user_sessions = GameSession.query.filter_by(user_id=user_id).all()
    if not user_sessions:
        return DifficultyLevel.EASY.value

    correct_answers = sum(session.correct_answers for session in user_sessions)
    total_questions = sum(session.total_questions for session in user_sessions)

    if total_questions == 0:
        return DifficultyLevel.EASY.value

    accuracy = correct_answers / total_questions

    if accuracy > 0.8:
        return DifficultyLevel.HARD.value
    elif accuracy > 0.5:
        return DifficultyLevel.MEDIUM.value
    else:
        return DifficultyLevel.EASY.value
