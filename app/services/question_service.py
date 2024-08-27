"""
Service layer for managing question-related operations.

This module contains functions to handle question creation, retrieval,
updating, and deletion, utilizing the Data Access Layer (DAL) to
perform database operations.
"""

from datetime import datetime
from app.dal.question_dal import QuestionDAL
from app.logging_config import logger
from sqlalchemy.exc import SQLAlchemyError
from app.services.gemini_service import adjust_game_difficulty
from app.services.openai_service import generate_trivia_question
from app.services.streaks_tracker import streaks
from app.models.gameSession import GameSession, db
from app.models.question import DifficultyLevel
from app.helpers.feedback_helper import increase_difficulty, decrease_difficulty
from app.services.score_service import create_score_service
from app.services.game_session_service import update_skill_mapping, check_for_milestones
from app.dal.game_session_dal import GameSessionDAL
from sqlalchemy.orm.attributes import flag_modified
from app.services.claude_service import get_hybrid_claude_feedback
from app.services.userProfile_service import award_experience_points, calculate_player_level, map_level_to_category
from app.models.userProfile import UserProfile


def get_question_by_id_service(question_id):
    """
    Service function to retrieve a question by its ID.

    Args:
        question_id (int): The ID of the question.

    Returns:
        tuple: Question data and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        question.times_asked += 1
        QuestionDAL.commit_changes()
        return question.to_dict(), 200
    except SQLAlchemyError as e:
        msg = f"Error retrieving question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_all_questions_service():
    """
    Service function to retrieve all questions.

    Returns:
        tuple: List of questions and status code.
    """
    try:
        questions = QuestionDAL.get_all_questions()
        return [question.to_dict() for question in questions], 200
    except SQLAlchemyError as e:
        msg = f"Error retrieving questions: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def update_question_service(question_id, question_data):
    """
    Service function to update a question.

    Args:
        question_id (int): The ID of the question to update.
        question_data (dict): Data for updating the question.

    Returns:
        tuple: Response message and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        QuestionDAL.update_question(question, **question_data)
        QuestionDAL.commit_changes()
        msg = f"Question ID: {question_id} updated successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 200
    except SQLAlchemyError as e:
        msg = f"Error updating question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def delete_question_service(question_id):
    """
    Service function to delete a question.

    Args:
        question_id (int): The ID of the question to delete.

    Returns:
        tuple: Response message and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        QuestionDAL.delete_question(question)
        msg = f"Question ID: {question_id} deleted successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 200
    except SQLAlchemyError as e:
        msg = f"Error deleting question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def update_streaks(user_id, correct):
    """
    Update the correct and incorrect streaks for a player.

    Args:
        user_id (int): The ID of the user.
        correct (bool): Whether the answer was correct.

    Returns:
        dict: The updated streaks for the user.
    """
    if user_id not in streaks:
        streaks[user_id] = {'correct_streak': 0, 'incorrect_streak': 0}

    if correct:
        streaks[user_id]['correct_streak'] += 1
        streaks[user_id]['incorrect_streak'] = 0
    else:
        streaks[user_id]['correct_streak'] = 0
        streaks[user_id]['incorrect_streak'] += 1

    return streaks[user_id]


def map_gemini_difficulty_to_enum(gemini_difficulty):
    """
    Maps the difficulty level suggested by Gemini to the predefined Enum difficulty levels.

    Args:
        gemini_difficulty (str or int): The difficulty level suggested by Gemini (e.g., 1, 2, ..., 10).

    Returns:
        DifficultyLevel: The corresponding Enum value for the question's difficulty.
    """
    if isinstance(gemini_difficulty, int):
        # Example logic to map difficulty levels 1-10 to 'easy', 'medium', 'hard'
        if gemini_difficulty <= 3:
            return DifficultyLevel.EASY
        elif 4 <= gemini_difficulty <= 7:
            return DifficultyLevel.MEDIUM
        else:
            return DifficultyLevel.HARD
    elif isinstance(gemini_difficulty, str):
        # If difficulty is already a string like 'easy', 'medium', 'hard'
        return DifficultyLevel[gemini_difficulty.upper()]
    else:
        # Default to medium if the input is not recognized
        return DifficultyLevel.MEDIUM


def submit_answer_service(session_id, question_id, user_id, correct, player_response):
    """
    Service function to handle submitting an answer, updating the success rate, and creating a score.

    Args:
        session_id (int): The ID of the game session.
        question_id (int): The ID of the question being answered.
        user_id (int): The ID of the user answering the question.
        correct (bool): Whether the answer was correct.
        player_response (str): The actual answer provided by the player.

    Returns:
        tuple: Response message and status code.
    """
    try:
        user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not user_profile:
            return {'status': 'fail', 'message': 'User profile not found.'}, 404

        player_level = calculate_player_level(user_profile.experience_points)
        player_level_category = map_level_to_category(player_level)

        if user_profile.level != player_level:
            user_profile.level = player_level
            db.session.commit()

        session = GameSessionDAL.get_game_session_by_id(user_id, session_id)
        if not session:
            return {'status': 'fail', 'message': f"Session ID: {session_id} not found."}, 404
        if session.questions_asked is None:
            session.questions_asked = []

        if session.response_times is None:
            session.response_times = {}

        if session.skill_levels is None:
            session.skill_levels = {}

        session = db.session.merge(session)
        start_time = datetime.utcnow()
        question = QuestionDAL.get_question_by_id(question_id)
        if not question:
            return {'status': 'fail', 'message': f"Question ID: {question_id} not found."}, 404

        if question_id not in session.questions_asked:
            session.questions_asked.append(question_id)
            flag_modified(session, "questions_asked")
            db.session.commit()

        if correct:
            session.correct_answers += 1
        session.total_questions += 1

        update_skill_mapping(session, question.category_id, correct, user_id)

        if 'skill_levels' in session.__dict__:
            flag_modified(session, "skill_levels")
        else:
            print("[ERROR] 'skill_levels' not found in session state!")
        db.session.commit()

        response_time = (datetime.utcnow() - start_time).total_seconds()
        session.response_times[str(question_id)] = response_time

        flag_modified(session, "response_times")

        GameSessionDAL.commit_changes()

        session = GameSessionDAL.get_game_session_by_id(user_id, session_id)

        question.times_asked += 1
        QuestionDAL.update_success_rate(question, correct)

        streak = update_streaks(user_id, correct)
        points = 10 if correct else 0
        if correct and streak['correct_streak'] >= 3:
            points += 5

        score_data = {
            'user_id': user_id,
            'score': points,
            'date': datetime.utcnow(),
            'category_id': question.category_id,
            'duration': session.get_duration()
        }
        create_score_service(score_data)

        achievements = check_for_milestones(user_id)
        if achievements:
            print(f"New achievements awarded: {achievements}")

        if correct:
            award_experience_points(user_profile, points=points)

        skill_levels = session.skill_levels
        past_performance = {
            question.category_id: {
                "struggles": skill_levels.get(str(question.category_id), {}).get("current_streak",
                                                                                 {}).get("incorrect", 0),
                "successes": skill_levels.get(str(question.category_id), {}).get("correct", 0)
            }
        }

        # Adjust difficulty using Gemini
        new_difficulty = adjust_game_difficulty(session, user_profile)
        print(f"New difficulty level set by Gemini: {new_difficulty}")

        # # Generate next question prompt
        # next_question_prompt = (
        #     f"Generate a unique and interesting trivia question at {new_difficulty} level. "
        #     f"Include a question, the correct answer, and three incorrect answers."
        # )
        #
        # next_question_data = generate_trivia_question(next_question_prompt)
        #
        # if next_question_data:
        #     cache_next_question(session_id, next_question_data)
        #     print(f"Cached next question for session {session_id}: {next_question_data}")

        feedback = get_hybrid_claude_feedback(
            player_name=user_profile.user.username,
            player_response=player_response,
            correct_answer=question.answer,
            question=question.question_text,
            question_category=question.category,
            question_type="True/False",
            player_level=player_level_category,
            correct=correct,
            past_performance=past_performance
        )

        print(f"Claude's Feedback: {feedback}")

        return {'status': 'success',
                'message': f"Question ID: {question_id} answered. Score recorded for session ID: {session_id}."}, 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'status': 'failed', 'message': f"Error processing answer or recording score: {str(e)}"}, 500
