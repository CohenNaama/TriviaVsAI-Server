# JSON schema to validate question creation
create_question_schema = {
    "type": "object",
    "properties": {
        "category_id": {"type": "integer", "minimum": 1},
        "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
        "question_text": {"type": "string", "minLength": 1},
        "answer": {"type": "string", "minLength": 1},
        "incorrect_answers": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 3
        }
    },
    "required": ["category_id", "difficulty", "question_text", "answer", "incorrect_answers"]
}

# JSON schema to validate question update
update_question_schema = {
    "type": "object",
    "properties": {
        "category_id": {"type": "integer", "minimum": 1},
        "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
        "question_text": {"type": "string", "minLength": 1},
        "answer": {"type": "string", "minLength": 1},
        "incorrect_answers": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 3
        }
    },
    "required": ["category_id", "difficulty", "question_text", "answer", "incorrect_answers"]
}
