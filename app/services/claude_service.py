"""
Claude Service Layer

This module provides services for generating feedback and insights using Claude, an AI-based system for enhancing user
experience in the game application. It manages the communication with Claude's API and processes the responses to
generate dynamic, personalized feedback for users based on their performance and game progress.

Key functionalities include:
- Generating personalized feedback for different player levels.
- Using templates and Claude's API to provide engaging and informative insights.
- Managing feedback length and variety to enhance user experience.
"""

import os
import logging
import anthropic
import random
from anthropic.types import TextBlock

logger = logging.getLogger(__name__)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

MAX_WORD_COUNT_NEW = 70
MAX_WORD_COUNT_INTERMEDIATE = 50
MAX_WORD_COUNT_ADVANCED = 30


system_prompt = (
    "You are an AI Game Coach providing real-time feedback to players. "
    "Your goal is to offer concise, engaging, and informative feedback based on the player's level:\n"
    "- For new players: Provide detailed explanations to help them understand the concepts.\n"
    "- For intermediate players: Offer quick tips and encouragement to reinforce their learning.\n"
    "- For advanced players: Keep the feedback concise, focusing on confirming their correct answers "
    "and challenging them to push further.\n"
    "Keep your responses between one to three sentences, depending on the player's needs."
)

feedback_templates = {
    "correct_new": [
        "Great job, {player_name}! {player_response} is correct. You're off to a strong start!",
        "Nice work, {player_name}! You got it right. Keep practicing, and you'll master this in no time!",
        "Well done, {player_name}! You're on the right track. Keep exploring!",
        "Fantastic! {player_response} is spot on. Keep up the good work, {player_name}!",
        "Excellent choice, {player_name}! {player_response} is the right answer. Your dedication is paying off!"
    ],
    "incorrect_new": [
        "Nice try, {player_name}. The correct answer was {correct_answer}. Don't worry, keep practicing!",
        "Good effort, {player_name}, but the correct answer was {correct_answer}. You'll get it next time!",
        "Almost there, {player_name}. The correct answer was {correct_answer}. Keep trying, and you'll improve!",
        "Not quite, {player_name}. The right answer was {correct_answer}. Keep pushing, and you'll get better!",
        "It's okay, {player_name}. The correct answer was {correct_answer}. Mistakes are just steps towards success!"
    ],
    "correct_intermediate": [
        "Well done, {player_name}! {player_response} is correct. You're improving quickly!",
        "Great work! {player_response} is right. You're mastering this topic!",
        "Excellent, {player_name}! You're getting stronger with each question.",
        "Spot on! {player_response} is correct. You're progressing well, {player_name}.",
        "Fantastic, {player_name}! {player_response} shows you're really grasping the material."
    ],
    "incorrect_intermediate": [
        "Almost there, {player_name}. The correct answer was {correct_answer}. Keep going!",
        "Not quite, {player_name}. The correct answer was {correct_answer}. You'll nail it next time!",
        "So close, {player_name}. The right answer was {correct_answer}. Keep it up!",
        "Good try, {player_name}, but the correct answer was {correct_answer}. You're learning fast!",
        "Don't be discouraged, {player_name}. The correct answer was {correct_answer}. Use this to fuel your "
        "next attempt!"
    ],
    "correct_advanced": [
        "Excellent, {player_name}! {player_response} is correct. You're really getting the hang of this!",
        "Spot on! {player_response} is correct. You're mastering this subject!",
        "Great work, {player_name}! {player_response} is right. You're at the top of your game!",
        "Impressive, {player_name}! {player_response} is correct. Keep challenging yourself!",
        "You're unstoppable, {player_name}! {player_response} was the perfect answer!"
    ],
    "incorrect_advanced": [
        "Good try, {player_name}. The correct answer was {correct_answer}. Challenge yourself with harder questions!",
        "Close, but not quite. The correct answer was {correct_answer}. Keep pushing your limits!",
        "Not quite right, {player_name}. The correct answer was {correct_answer}. You're almost there!",
        "You almost had it, {player_name}. The correct answer was {correct_answer}. Keep up the hard work!",
        "Even the best make mistakes, {player_name}. The correct answer was {correct_answer}. Learn from this "
        "and excel!"
    ]
}

performance_feedback_templates = {
    "positive": [
        "You're usually great at this category! Don't let this one slip-up get you down—keep pushing forward!",
        "You've nailed this category before! Stay focused, and you'll get it right next time!",
        "Keep up the good work! You're performing well overall in this category.",
        "Remember, you're doing well in this category. Keep your spirits high and continue!",
        "Don't worry about this small mistake; your overall performance in this category is strong!"
    ],
    "constructive": [
        "Keep working on this category. Every mistake is a chance to learn and improve!",
        "This category might be challenging, but persistence is key. Keep at it!",
        "Mistakes happen to everyone. Focus on learning from them and improving!",
        "Stay positive! Use this as a learning opportunity to get better in this category.",
        "Keep pushing through! With more practice, this category will become easier."
    ]
}


def get_claude_feedback(question, player_response, correct_answer, player_level, question_category,
                        question_type="multiple choice",):
    """
    Generates dynamic feedback from Claude based on the player's response, question details, and player level.
    Args:
        player_response (str): The player's response.
        correct_answer (str): The correct answer to the question.
        question (str): The question text.
        question_type (str): The type of question ("multiple choice").
        player_level (str): The player's level ("new", "intermediate", "advanced").
        question_category (Category, optional): The category object of the question.
    Returns:
        str: Feedback generated by Claude.
    """
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    prompt_types = [
        "Provide a brief historical context related to the answer.",
        "Share a fun fact related to the answer to engage the player.",
        "Explain why this answer is significant or interesting.",
        "Offer a practical application of the knowledge related to this answer."
    ]

    chosen_prompt = random.choice(prompt_types)

    prompt = (
        f"The question was: '{question}'.\n"
        f"The player responded: '{player_response}'.\n"
        f"The correct answer is: '{correct_answer}'.\n"
        f"The player's level is '{player_level}'.\n"
        f"This was a question in the category '{question_category.name}' and is of type '{question_type}'.\n"
        f"{chosen_prompt} Provide feedback that is engaging, educational, and tailored to the player's level."
    )
    print("prompt from get_claude_feedback:", prompt)

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=100,
        temperature=0.9,
        system=system_prompt,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    feedback = response.content
    return feedback


def generate_feedback_from_template(player_name, player_response, correct_answer, player_level, correct):
    """
    Generates feedback using predefined templates based on the player's level and the correctness of their response.

    Args:
        player_name (str): The name of the player.
        player_response (str): The player's answer.
        correct_answer (str): The correct answer to the question.
        player_level (str): The player's level ("new", "intermediate", "advanced").
        correct (bool): Indicates if the player's response was correct.

    Returns:
        str: Feedback generated from templates.
    """
    if player_level == "new":
        feedback_type = "correct_new" if correct else "incorrect_new"
    elif player_level == "intermediate":
        feedback_type = "correct_intermediate" if correct else "incorrect_intermediate"
    else:
        feedback_type = "correct_advanced" if correct else "incorrect_advanced"

    template = random.choice(feedback_templates[feedback_type])
    feedback = template.format(player_name=player_name, player_response=player_response, correct_answer=correct_answer)
    return feedback


def truncate_feedback(feedback, max_word_count=None, max_char_count=None):
    """
    Truncates feedback to ensure it does not exceed specified word or character limits.

    Args:
        feedback (str): The full feedback text.
        max_word_count (int, optional): The maximum number of words allowed in the feedback.
        max_char_count (int, optional): The maximum number of characters allowed in the feedback.

    Returns:
        str: Truncated feedback.
    """
    if max_word_count:
        words = feedback.split()
        if len(words) > max_word_count:
            feedback = ' '.join(words[:max_word_count])
            if not feedback.endswith('.'):
                feedback = feedback.rsplit('.', 1)[0] + '.'
            feedback += '...'
    elif max_char_count:
        if len(feedback) > max_char_count:
            feedback = feedback[:max_char_count]
            if not feedback.endswith('.'):
                feedback = feedback.rsplit('.', 1)[0] + '.'
            feedback += '...'
    return feedback


def get_hybrid_claude_feedback(player_name, player_response, correct_answer, question, question_category, question_type,
                               player_level, correct, past_performance):
    """
    Combines template-based feedback with dynamic insights from Claude, tailored to the player's level.

    Args:
        player_name (str): The name of the player.
        player_response (str): The player's response.
        correct_answer (str): The correct answer to the question.
        question (str): The question object containing details about the question.
        question_category (Category, optional): The category object of the question.
        question_type (str): The type of question (e.g., "multiple choice").
        player_level (str): The player's level ("new", "intermediate", "advanced").
        correct (bool): Indicates if the player's response was correct.
        past_performance (dict): Contains player's past performance metrics like struggles and successes.

    Returns:
        str: Combined feedback from templates and Claude's insights.
    """

    feedback = generate_feedback_from_template(player_name, player_response, correct_answer, player_level, correct)

    claude_insight = get_claude_feedback(question, player_response, correct_answer, player_level, question_category,
                                         question_type)

    if isinstance(claude_insight, list) and len(claude_insight) > 0 and isinstance(claude_insight[0], TextBlock):
        claude_text = claude_insight[0].text
    else:
        claude_text = claude_insight

    if correct:
        full_feedback = f"{feedback}\n\nDetailed explanation: {claude_text}"
    else:
        if past_performance[question_category.id]["successes"] > past_performance[question_category.id]["struggles"]:
            additional_feedback = random.choice(performance_feedback_templates["positive"])
        else:
            additional_feedback = random.choice(performance_feedback_templates["constructive"])

        full_feedback = f"{feedback}\n{additional_feedback}\n\nDetailed explanation: {claude_text}"

    if player_level == "new":
        full_feedback = truncate_feedback(full_feedback, max_word_count=100)
    elif player_level == "intermediate":
        full_feedback = truncate_feedback(full_feedback, max_word_count=70)
    else:
        full_feedback = truncate_feedback(full_feedback, max_word_count=50)

    return full_feedback
