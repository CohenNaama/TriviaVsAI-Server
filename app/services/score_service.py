"""
Service layer for managing score-related operations.

This module provides functions to handle the creation, retrieval, and deletion
of categories. It interacts with the Score Data Access Layer (DAL) to perform
database operations and manage score-related business logic.
"""

from app.dal.score_dal import ScoreDAL
from app.models.score import Score


def create_score_service(score_data):
    """
    Service function to create a new score.

    Args:
        score_data (dict): Data for creating a new score.

    Returns:
        dict: Response message and status code.
    """
    try:
        score = ScoreDAL.create_score(score_data)
        return {'status': 'success',
                'message': 'Score created successfully.',
                'data': score.to_dict()}, 201
    except Exception as e:
        return {'status': 'failed', 'message': f"Error creating score: {str(e)}"}, 500


def get_score_service(user_id, score_id):
    """
    Service function to retrieve a score by its ID and user ID.

    Args:
        user_id (int): The ID of the user.
        score_id (int): The ID of the score.

    Returns:
        dict: Response message and status code.
    """
    try:
        score = ScoreDAL.get_score_by_id(user_id, score_id)
        if not score:
            return {'status': 'failed', 'message': 'Score not found.'}, 404
        return {'status': 'success', 'data': score.to_dict()}, 200
    except Exception as e:
        return {'status': 'failed', 'message': f"Error retrieving score: {str(e)}"}, 500


def get_all_scores_of_user_service(user_id):
    """
    Service function to retrieve all scores of the user.

    Returns:
        dict: Response message and status code.
    """
    try:
        scores = ScoreDAL.get_all_scores_of_user(user_id)
        return {'status': 'success',
                'data': [score.to_dict() for score in scores]}, 200
    except Exception as e:
        return {'status': 'failed',
                'message': f"Error retrieving scores: {str(e)}"}, 500


def get_all_scores_service():
    """
    Service function to retrieve all scores.

    Returns:
        dict: Response message and status code.
    """
    try:
        scores = ScoreDAL.get_all_scores()
        return {'status': 'success',
                'data': [score.to_dict() for score in scores]}, 200
    except Exception as e:
        return {'status': 'failed',
                'message': f"Error retrieving scores: {str(e)}"}, 500


def update_score_service(score_id, user_id, data):
    """
    Update an existing score in the database.

    Args:
        score_id (int): The ID of the score to update.
        user_id (int): The ID of the user who owns the score.
        data (dict): The new data for the score.

    Returns:
        Score: The updated Score object.
    """
    try:
        updated_score = ScoreDAL.update_score(score_id, user_id, data)
        return {'status': 'success',
                'message': 'Score updated successfully.',
                'data': updated_score.to_dict()}, 204
    except Exception as e:
        return {'status': 'failed', 'message': f"Error updating score: {str(e)}"}, 500


def delete_score_service(user_id, score_id):
    """
    Service function to delete a score.

    Args:
        user_id (int): The ID of the user who owns the score.
        score_id (int): The ID of the score to delete.

    Returns:
        dict: Response message and status code.
    """
    try:
        result = ScoreDAL.delete_score(score_id, user_id)
        if not result:
            return {'status': 'failed',
                    'message': 'Score not found.'}, 404
        return {'status': 'success',
                'message': 'Score deleted successfully.'}, 204
    except Exception as e:
        return {'status': 'failed',
                'message': f"Error deleting score: {str(e)}"}, 500
