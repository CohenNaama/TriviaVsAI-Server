from flask import Blueprint, jsonify
from app.services.leaderboard_service import get_leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/leaderboard', methods=['GET'])
def leaderboard_route():
    """
    API endpoint to get the global leaderboard.

    Returns:
        Response: JSON response containing the leaderboard rankings.
    """
    leaderboard = get_leaderboard()
    return jsonify(leaderboard), 200
