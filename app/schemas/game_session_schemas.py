# JSON schema to validate game session creation
create_game_session_schema = {
    "type": "object",
    "properties": {
        "questions_asked": {"type": "array", "items": {"type": "integer"}},
        "correct_answers": {"type": "integer", "minimum": 0},
        "total_questions": {"type": "integer", "minimum": 1},
        "start_time": {"type": "string", "format": "date-time"},
        "end_time": {"type": "string", "format": "date-time"}
    },
    "required": ["questions_asked", "correct_answers", "total_questions"]
}

# JSON schema to validate game session update
update_game_session_schema = {
    "type": "object",
    "properties": {
        "questions_asked": {"type": "array", "items": {"type": "integer"}},
        "correct_answers": {"type": "integer", "minimum": 0},
        "total_questions": {"type": "integer", "minimum": 1},
        "start_time": {"type": "string", "format": "date-time"},
        "end_time": {"type": "string", "format": "date-time"}
    }
}
