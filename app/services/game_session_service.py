"""
Service layer for managing game session-related operations.

This module provides functions to handle the creation, retrieval, and deletion
of game sessions. It interacts with the GameSession Data Access Layer (DAL) to perform
database operations and manage game session-related business logic.
"""

from app.dal.game_session_dal import GameSessionDAL
from datetime import datetime
from app.models.gameSession import db


def create_game_session_service(session_data):
    """
    Service function to create a new game session.

    Args:
        session_data (dict): Data for creating a new game session.

    Returns:
        dict: Response message and status code.
    """
    try:
        session = GameSessionDAL.create_game_session(session_data)
        return {'status': 'success',
                'message': 'Game session created successfully.',
                'data': session.to_dict()}, 201
    except Exception as e:
        return {'status': 'failed', 'message': f"Error creating game session: {str(e)}"}, 500


def get_game_session_service(user_id, session_id):
    """
    Service function to retrieve a game session by its ID and user ID.

    Args:
        user_id (int): The ID of the user.
        session_id (int): The ID of the game session.

    Returns:
        dict: Response message and status code.
    """
    try:
        session = GameSessionDAL.get_game_session_by_id(user_id, session_id)
        if not session:
            return {'status': 'failed', 'message': 'Game session not found.'}, 404
        return {'status': 'success', 'data': session.to_dict()}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving game session: {str(e)}"}, 500


def get_all_game_sessions_of_user_service(user_id):
    """
    Service function to retrieve all game sessions of a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Response message and status code.
    """
    try:
        sessions = GameSessionDAL.get_all_game_sessions_of_user(user_id)
        if not sessions:
            return {'status': 'success', 'data': []}, 200
        return {'status': 'success', 'data': [session.to_dict() for session in sessions]}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving game sessions: {str(e)}"}, 500


def get_all_game_sessions_service():
    """
    Service function to retrieve all game sessions.

    Returns:
        dict: Response message and status code.
    """
    try:
        sessions = GameSessionDAL.get_all_game_sessions()
        if not sessions:
            return {'status': 'success', 'data': []}, 200
        return {'status': 'success', 'data': [session.to_dict() for session in sessions]}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving game sessions: {str(e)}"}, 500


def update_game_session_service(session_id, user_id, data):
    """
    Service function to update a game session.

    Args:
        session_id (int): The ID of the game session to update.
        user_id (int): The ID of the user who owns the game session.
        data (dict): The new data for the game session.

    Returns:
        dict: Response message and status code.
    """
    try:
        updated_session = GameSessionDAL.update_game_session(session_id, user_id, data)
        return {'status': 'success', 'message': 'Game session updated successfully.', 'data': updated_session.to_dict()}, 204
    except Exception as e:
        return {'status': 'failed', 'message': f"Error updating game session: {str(e)}"}, 500


def delete_game_session_service(user_id, session_id):
    """
    Service function to delete a game session.

    Args:
        user_id (int): The ID of the user who owns the game session.
        session_id (int): The ID of the game session to delete.

    Returns:
        dict: Response message and status code.
    """
    try:
        result = GameSessionDAL.delete_game_session(session_id, user_id)
        if not result:
            return {'status': 'failed', 'message': 'Game session not found.'}, 404
        return {'status': 'success', 'message': 'Game session deleted successfully.'}, 204
    except Exception as e:
        return {'status': 'failed', 'message': f"Error deleting game session: {str(e)}"}, 500


def update_skill_mapping(session, category_id, correct):
    """
    Update the user's skill level mapping based on performance in a category.

    Args:
        session (GameSession): The current game session object.
        category_id (int): The category ID.
        correct (bool): Whether the answer was correct.

    Returns:
        None
    """
    skill_levels = session.skill_levels or {}

    skill_levels.setdefault(str(category_id), {
        'correct': 0,
        'total': 0,
        'current_streak': {'correct': 0, 'incorrect': 0},
        'max_streak': {'correct': 0, 'incorrect': 0},
        'accuracy': 0.0,
        'last_attempt_correct': None
    })

    skill_levels[str(category_id)].setdefault('current_streak', {'correct': 0, 'incorrect': 0})
    skill_levels[str(category_id)].setdefault('max_streak', {'correct': 0, 'incorrect': 0})

    skill_levels[str(category_id)]['total'] += 1

    if correct:
        skill_levels[str(category_id)]['correct'] += 1
        skill_levels[str(category_id)]['current_streak']['correct'] += 1
        skill_levels[str(category_id)]['current_streak']['incorrect'] = 0

        if (skill_levels[str(category_id)]['current_streak']['correct'] >
                skill_levels[str(category_id)]['max_streak']['correct']):
            skill_levels[str(category_id)]['max_streak']['correct'] = (
                skill_levels)[str(category_id)]['current_streak']['correct']
    else:
        skill_levels[str(category_id)]['current_streak']['incorrect'] += 1
        skill_levels[str(category_id)]['current_streak']['correct'] = 0

        if (skill_levels[str(category_id)]['current_streak']['incorrect'] >
                skill_levels[str(category_id)]['max_streak']['incorrect']):
            skill_levels[str(category_id)]['max_streak']['incorrect'] = (
                skill_levels)[str(category_id)]['current_streak']['incorrect']

    skill_levels[str(category_id)]['accuracy'] = (
            skill_levels[str(category_id)]['correct'] / skill_levels[str(category_id)]['total'])

    skill_levels[str(category_id)]['last_attempt_correct'] = correct

    session.skill_levels = skill_levels
    db.session.add(session)
    db.session.flush()


def finalize_session_service(session_id, user_id):
    """
    Service function to finalize a game session.

    Args:
        session_id (int): The ID of the game session.
        user_id (int): The ID of the user.

    Returns:
        dict: A response message and status code.
    """
    session = GameSessionDAL.get_game_session_by_id(user_id, session_id)
    if not session:
        return {"status": "failed", "message": f"Session ID {session_id} not found."}, 404

    if session.is_finalized:
        return {"status": "failed", "message": "Session is already finalized."}, 400

    try:
        GameSessionDAL.finalize_session(session)
        return {"status": "success", "message": f"Session ID {session_id} finalized successfully."}, 200
    except Exception as e:
        return {"status": "failed", "message": f"Error finalizing session ID {session_id}: {str(e)}"}, 500


def terminate_session_service(session_id, user_id, reason="completed", user_initiated=False):
    """
    Terminate a game session based on specific criteria.

    Args:
        session_id (int): The ID of the session to terminate.
        reason (str): The reason for termination, e.g., "completed", "incorrect_answers", "manual_exit".
        user_initiated (bool): Whether the termination was initiated by the user.

    Returns:
        dict: Response message and status code.
    """
    session = GameSessionDAL.get_game_session_by_id(user_id, session_id)
    if not session:
        return {"status": "failed", "message": f"Session ID {session_id} not found."}, 404

    if not session.is_finalized:
        finalize_session_service(user_id, session_id)

    session.is_active = False
    session.termination_reason = reason
    session.user_initiated = user_initiated
    session.end_time = datetime.utcnow()

    data = {
        'is_active': session.is_active,
        'termination_reason': session.termination_reason,
        'user_initiated': session.user_initiated,
        'end_time': session.end_time
    }

    try:
        GameSessionDAL.update_game_session(session_id, user_id, data)
        GameSessionDAL.commit_changes()
        return {"status": "success", "message": f"Session ID {session_id} terminated due to {reason}."}, 200
    except Exception as e:
        return {"status": "failed", "message": f"Error terminating session ID {session_id}: {str(e)}"}, 500


def check_incorrect_answers(user_id, session_id, incorrect_count):
    if incorrect_count >= 3:
        terminate_session_service(user_id, session_id, reason="incorrect_answers")
