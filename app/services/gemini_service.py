"""
Gemini Service Layer

This module provides services for dynamically adjusting the difficulty level of questions in the game application
using Gemini, an AI-based system designed to enhance adaptive learning experiences. It interacts with the Gemini API
to analyze player performance data and recommends appropriate difficulty levels for subsequent questions, thereby
maintaining an optimal challenge for users.

Key functionalities include:
- Analyzing player performance and skill levels to adjust the difficulty dynamically.
- Communicating with the Gemini API to obtain difficulty level recommendations.
- Caching difficulty recommendations to improve efficiency and minimize redundant API calls.
- Handling various types of responses and errors from the Gemini API to ensure smooth operation.
- Providing a fallback mechanism to set default difficulty levels in case of unexpected responses or API errors.
"""


import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from app.models.question import DifficultyLevel
from app.services.streaks_tracker import get_streaks
from app.logging_config import logger
from google.api_core.exceptions import (GoogleAPIError, InvalidArgument, PermissionDenied, NotFound, ResourceExhausted,
                                        InternalServerError, ServiceUnavailable, DeadlineExceeded)


load_dotenv()


genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

gemini_model = genai.GenerativeModel('gemini-1.5-flash')

gemini_cache = {}


def generate_gemini_content(prompt):
    """
    Generate content using the Gemini API.

    Args:
        prompt (str): The prompt text for generating content.

    Returns:
        str: Generated content from Gemini.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except (InvalidArgument, PermissionDenied, NotFound) as e:
        print(f"Client error occurred: {e}")
    except (ResourceExhausted, InternalServerError, ServiceUnavailable, DeadlineExceeded) as e:
        print(f"Server error occurred: {e}")
    except GoogleAPIError as e:
        print(f"API error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


def map_gemini_difficulty_to_enum(gemini_difficulty):
    """
    Maps the difficulty level suggested by Gemini to the predefined Enum difficulty levels.

    Args:
        gemini_difficulty (str): The difficulty level suggested by Gemini (e.g., '1', '2', ..., '10').

    Returns:
        DifficultyLevel: The corresponding Enum value for the question's difficulty.
    """
    if gemini_difficulty.isdigit():
        gemini_difficulty = int(gemini_difficulty)
        if gemini_difficulty <= 3:
            return DifficultyLevel.EASY
        elif 4 <= gemini_difficulty <= 7:
            return DifficultyLevel.MEDIUM
        else:
            return DifficultyLevel.HARD
    else:
        return DifficultyLevel[gemini_difficulty.upper()]


def extract_difficulty_from_response(response_text):
    """
    Extract the difficulty level from Gemini's response.

    Args:
        response_text (str): The raw response text from Gemini.

    Returns:
        str: Extracted difficulty level (EASY, MEDIUM, HARD), or None if not found.
    """
    for difficulty in ["EASY", "MEDIUM", "HARD"]:
        if difficulty in response_text.upper():
            return difficulty
    return None


def adjust_game_difficulty(session, user_profile):
    """
    Adjust the game difficulty dynamically using Gemini based on player performance and session data.

    Args:
        session (GameSession): The current game session.
        user_profile (UserProfile): The user's profile containing performance data.

    Returns:
        str: New difficulty level based on AI recommendations.
    """
    streak_info = get_streaks(user_profile.user_id)
    correct_streak = streak_info.get('correct_streak', 0)

    total_questions = session.total_questions
    correct_answers = session.correct_answers
    skill_levels = session.skill_levels

    average_response_time = sum(session.response_times.values()) / len(
        session.response_times) if session.response_times else 0

    prompt = (
        f"Based on a player with a level of {user_profile.level}, a correct streak of {correct_streak}, "
        f"having answered {total_questions} questions, with {correct_answers} correct answers, "
        f"and skill levels as follows: {skill_levels}. The average response time for the player is "
        f"{average_response_time:.2f} seconds. "
        f"What should the next question's difficulty be? Please provide a concise response (no more than 20 words) "
        f"recommending the next question's difficulty. "
        "Respond only with one of the following options: EASY, MEDIUM, or HARD."
    )

    recommended_difficulty = generate_gemini_content(prompt)

    if recommended_difficulty:
        difficulty_level = extract_difficulty_from_response(recommended_difficulty)
        if difficulty_level:
            gemini_cache[session.id] = {
                'difficulty': difficulty_level,
                'timestamp': datetime.utcnow()
            }
            logger.debug(f"gemini_cache: {gemini_cache}")
            return difficulty_level

    logger.warning(f"Unexpected difficulty level from Gemini: {recommended_difficulty}")
    return "EASY"
