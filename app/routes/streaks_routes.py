from flask import Blueprint, jsonify, request
from app.services.streaks_tracker import get_streaks

streak_bp = Blueprint('streak_bp', __name__)


@streak_bp.route('/streaks/<int:user_id>', methods=['GET'])
def get_user_streaks(user_id):
    """
    API endpoint to retrieve the current streaks for a given user.

    Returns:
        Response: JSON response with the user's current streaks.
    """
    streak = get_streaks(user_id)
    return jsonify(streak), 200
