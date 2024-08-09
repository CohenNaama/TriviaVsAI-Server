from flask import Blueprint, request, jsonify
from app.services.openai_service import create_question_with_ai
from app.middleware.decorators import admin_required, json_validator

openai_bp = Blueprint('openai_bp', __name__)


@openai_bp.route('/questions/ai', methods=['POST'])
@admin_required()
# @json_validator(schema=create_question_schema)
def create_question_route():
    """
    API endpoint to create a question using AI.

    Returns:
        Response: JSON response with the created question or error message.
    """
    data = request.json
    response, status = create_question_with_ai(data)
    return jsonify(response), status
