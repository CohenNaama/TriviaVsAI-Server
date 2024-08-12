def increase_difficulty(current_difficulty):
    """
    Increase the difficulty level of questions.

    Args:
        current_difficulty (str): The current difficulty level.

    Returns:
        str: The new, increased difficulty level.
    """
    difficulty_levels = ['easy', 'medium', 'hard']

    try:
        current_index = difficulty_levels.index(current_difficulty.lower())
        if current_index < len(difficulty_levels) - 1:
            return difficulty_levels[current_index + 1]
        else:
            return current_difficulty
    except ValueError:
        return 'medium'


def decrease_difficulty(current_difficulty):
    """
    Decrease the difficulty level of questions.

    Args:
        current_difficulty (str): The current difficulty level.

    Returns:
        str: The new, decreased difficulty level.
    """
    difficulty_levels = ['easy', 'medium', 'hard']

    try:
        current_index = difficulty_levels.index(current_difficulty.lower())
        if current_index > 0:
            return difficulty_levels[current_index - 1]
        else:
            return current_difficulty
    except ValueError:
        return 'medium'
