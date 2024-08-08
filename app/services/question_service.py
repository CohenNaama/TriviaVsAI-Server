"""
Service layer for managing question-related operations.

This module contains functions to handle question creation, retrieval,
updating, and deletion, utilizing the Data Access Layer (DAL) to
perform database operations.
"""

import openai
import os
from datetime import datetime
from app.dal.question_dal import QuestionDAL
from app.models.question import DifficultyLevel, Question
from app.logging_config import logger
from sqlalchemy.exc import SQLAlchemyError


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

        # Split the response by lines
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

        # Ensure the correct answer is extracted properly
        if answer == "" and incorrect_answers:
            answer = incorrect_answers.pop(0).replace("Correct Answer:", "").strip()

        logger.debug(f"Parsed question: {question_text}")
        logger.debug(f"Parsed answer: {answer}")
        logger.debug(f"Parsed incorrect answers: {incorrect_answers}")

        # Ensure at least three incorrect answers
        while len(incorrect_answers) < 3:
            incorrect_answers.append("Unknown Incorrect Answer")

        return {
            "question_text": question_text,
            "answer": answer,
            "incorrect_answers": incorrect_answers[:3],  # Ensure only three incorrect answers
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
        logger.debug(f"Using OpenAI API Key: {openai.api_key}")

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
        logger.debug(f"OpenAI response: {response_text}")

        question_data = parse_ai_response(response_text)
        return question_data

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise


def create_question_with_ai(data):
    """
    Create a question using AI-generated content.

    Args:
        data (dict): Initial question data.

    Returns:
        tuple: Response message and status code.
    """
    try:
        prompt = (
            f"Generate a unique and interesting trivia question about {data['category']} "
            f"at {data['difficulty']} level. Include a question, the correct answer, and "
            "three incorrect answers. Ensure the topic is distinct from previous requests."
        )

        question_data = generate_trivia_question(prompt)

        if not is_question_unique(question_data['question_text']):
            msg = "Duplicate question detected."
            logger.warning(msg)
            return {'status': 'failed', 'message': msg}, 409

        question_data.update({
            "category_id": data["category_id"],
            "difficulty": DifficultyLevel[data["difficulty"].upper()],
            "created_at": datetime.utcnow()
        })

        question = QuestionDAL.create_question(question_data)
        QuestionDAL.commit_changes()

        logger.info(f"AI-generated question created successfully: {question}")
        return {'status': 'success',
                'message': 'AI-generated question created successfully.',
                'data': question.to_dict()}, 201
    except Exception as e:
        msg = f"Error creating AI-generated question: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_question_by_id_service(question_id):
    """
    Service function to retrieve a question by its ID.

    Args:
        question_id (int): The ID of the question.

    Returns:
        tuple: Question data and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        return question.to_dict(), 200
    except SQLAlchemyError as e:
        msg = f"Error retrieving question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def get_all_questions_service():
    """
    Service function to retrieve all questions.

    Returns:
        tuple: List of questions and status code.
    """
    try:
        questions = QuestionDAL.get_all_questions()
        return [question.to_dict() for question in questions], 200
    except SQLAlchemyError as e:
        msg = f"Error retrieving questions: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def update_question_service(question_id, question_data):
    """
    Service function to update a question.

    Args:
        question_id (int): The ID of the question to update.
        question_data (dict): Data for updating the question.

    Returns:
        tuple: Response message and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        QuestionDAL.update_question(question, **question_data)
        QuestionDAL.commit_changes()
        msg = f"Question ID: {question_id} updated successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 200
    except SQLAlchemyError as e:
        msg = f"Error updating question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500


def delete_question_service(question_id):
    """
    Service function to delete a question.

    Args:
        question_id (int): The ID of the question to delete.

    Returns:
        tuple: Response message and status code.
    """
    try:
        question = QuestionDAL.get_question_by_id(question_id)
        if question is None:
            msg = f"Question ID: {question_id} not found."
            logger.info(msg)
            return {'status': 'fail', 'message': msg}, 404

        QuestionDAL.delete_question(question)
        msg = f"Question ID: {question_id} deleted successfully."
        logger.info(msg)
        return {'status': 'success', 'message': msg}, 200
    except SQLAlchemyError as e:
        msg = f"Error deleting question ID {question_id}: {str(e)}"
        logger.error(msg)
        return {'status': 'failed', 'message': msg}, 500
