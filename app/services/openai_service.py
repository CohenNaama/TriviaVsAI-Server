"""
OpenAI Service Layer

This module provides services for generating trivia questions using OpenAI's API. It interacts with the OpenAI API
to create dynamic and engaging questions for users in the game application, based on specific prompts and categories.

Key functionalities include:
- Parsing AI-generated responses to extract trivia questions, correct answers, and incorrect options.
- Ensuring generated questions are unique and do not repeat within the same session.
- Adjusting question difficulty based on player performance and game progress.
- Managing interactions with the OpenAI API and handling API-related errors.

This service is essential for dynamically generating content that enhances user engagement and provides a tailored
experience based on individual player progress and preferences.
"""

import openai
import os
from datetime import datetime
from app.logging_config import logger
from app.models.question import Question
from app.models.gameSession import GameSession
from app.dal.question_dal import QuestionDAL
from app.models.userProfile import UserProfile
from app.services.gemini_service import adjust_game_difficulty
from app.services.category_service import select_category
from app.services.gemini_service import gemini_cache

openai.api_key = os.getenv('OPENAI_API_KEY')


def parse_ai_response(response_text):
    """
    Parse the AI response to extract question, correct answer, and incorrect answers.

    Args:
        response_text (str): The raw response text from AI.

    Returns:
        dict: Parsed question data.
    """
    try:
        lines = [line.strip() for line in response_text.split('\n') if line.strip()]
        logger.debug(f"Parsed lines: {lines}")

        question_text = ""
        answer = ""
        incorrect_answers = []

        for line in lines:
            if line.lower().startswith("question:"):
                question_text = line.replace("Question:", "").strip()
            elif line.lower().startswith("answer:"):
                answer = line.replace("Answer:", "").strip()
            elif line.lower().startswith("incorrect answers:"):
                continue  # Skip the header
            else:
                incorrect_answers.append(line.replace("Incorrect Answer", "")
                                         .replace(f"{len(incorrect_answers) + 1}.", "").strip())

        if answer == "" and incorrect_answers:
            answer = incorrect_answers.pop(0).replace("Correct Answer:", "").strip()

        logger.debug(f"Parsed question: {question_text}")
        logger.debug(f"Parsed answer: {answer}")
        logger.debug(f"Parsed incorrect answers: {incorrect_answers}")

        while len(incorrect_answers) < 3:
            incorrect_answers.append("Unknown Incorrect Answer")

        return {
            "question_text": question_text,
            "answer": answer,
            "incorrect_answers": incorrect_answers[:3],
        }
    except Exception as e:
        logger.error(f"Error parsing AI response: {e}")
        return {
            "question_text": "Unknown Question",
            "answer": "Unknown Answer",
            "incorrect_answers": ["Incorrect 1", "Incorrect 2", "Incorrect 3"],
        }


def is_question_unique(question_text):
    """
    Check if a question is unique in the database.

    Args:
        question_text (str): The question text to check.

    Returns:
        bool: True if the question is unique, False otherwise.
    """
    existing_question = Question.query.filter_by(question_text=question_text).first()

    if existing_question:
        logger.debug(f"Duplicate question detected: {question_text}")
        return False
    else:
        logger.debug(f"Unique question: {question_text}")
        return True


def generate_trivia_question(prompt):
    """
    Generate a trivia question using OpenAI.

    Args:
        prompt (str): The prompt for generating trivia questions.

    Returns:
        dict: A dictionary containing the question, answer, and incorrect answers.
    """
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a trivia question generator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
            n=1
        )

        response_text = response['choices'][0]['message']['content'].strip()

        question_data = parse_ai_response(response_text)
        return question_data

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise


def create_question_for_session_service(user_id, session_id):
    """
    Service function to create the next AI-generated question for the user, adjusting difficulty as needed,
    and ensuring no repeated questions within the same session.

    Args:
        user_id (int): The ID of the user.
        session_id (int): The ID of the game session.

    Returns:
        dict: A dictionary containing the next question and its difficulty level.
    """
    try:
        session = GameSession.query.get(session_id)
        if session is None:
            raise Exception(f"Session ID {session_id} not found.")

        # Check if there's a cached difficulty for this session
        if session_id in gemini_cache:
            adjusted_difficulty = gemini_cache[session_id]['difficulty']
            print(f"Using cached difficulty level: {adjusted_difficulty}")
        else:
            # Use Gemini's recommendation to adjust difficulty
            user_profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not user_profile:
                raise Exception(f"User profile for ID {user_id} not found.")

            # Call the new Gemini-based function
            adjusted_difficulty = adjust_game_difficulty(session, user_profile)

        selected_category = select_category()

        prompt = (
            f"Generate a unique and interesting trivia question about {selected_category.name} "
            f"at difficulty level {adjusted_difficulty}. Include a question, the correct answer, and "
            "three incorrect answers."
        )

        question_data = generate_trivia_question(prompt)

        if not is_question_unique(question_data['question_text']):
            raise Exception("Duplicate question detected.")

        question_data.update({
            "category_id": selected_category.id,
            "difficulty": adjusted_difficulty,
            "created_at": datetime.utcnow()
        })

        question = QuestionDAL.create_question(question_data)

        session.questions_asked.append(question.id)
        session.total_questions += 1

        QuestionDAL.commit_changes()

        return {'question': question.to_dict(), 'difficulty': adjusted_difficulty}

    except Exception as e:
        raise Exception(f"Failed to generate the next question: {str(e)}")
