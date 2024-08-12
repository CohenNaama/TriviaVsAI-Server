# Global dictionary to track streaks for each user during a session
streaks = {}


def get_streaks(user_id):
    """
    Retrieve the current streaks for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the current correct and incorrect streaks.
    """
    return streaks.get(user_id, {'correct_streak': 0, 'incorrect_streak': 0})
