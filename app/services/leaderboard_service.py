from app.dal.score_dal import ScoreDAL


def get_leaderboard():
    """
    Generate a leaderboard based on total score.

    Returns:
        list: A list of dictionaries representing user rankings.
    """
    leaderboard = ScoreDAL.fetch_leaderboard()

    leaderboard_dict = [
        {"username": row.username, "total_score": row.total_score} for row in leaderboard
    ]

    return leaderboard_dict
