"""
Service layer for managing game session-related operations.

This module provides functions to handle the creation, retrieval, and deletion
of game sessions. It interacts with the GameSession Data Access Layer (DAL) to perform
database operations and manage game session-related business logic.
"""

from app.dal.game_session_dal import GameSessionDAL


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
