# JSON schema to validate score creation
create_score_schema = {
    "type": "object",
    "properties": {
        # "user_id": {"type": "integer", "minimum": 1},
        "score": {"type": "integer", "minimum": 0},
        "category_id": {"type": "integer", "minimum": 1},
        "duration": {"type": "integer", "minimum": 0}
    },
    "required": ["score", "category_id", "duration"]
}


# JSON schema to validate score update
update_score_schema = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "minimum": 0},
        "category_id": {"type": "integer", "minimum": 1},
        "duration": {"type": "integer", "minimum": 0}
    },
    "required": ["score", "category_id", "duration"]
}
