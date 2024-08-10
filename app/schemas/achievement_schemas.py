# JSON schema to validate achievement creation
create_achievement_schema = {
    "type": "object",
    "properties": {
        "achievement_name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "date_awarded": {"type": "string", "format": "date-time"}
    },
    "required": ["achievement_name"]
}

# JSON schema to validate achievement update
update_achievement_schema = {
    "type": "object",
    "properties": {
        "achievement_name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "date_awarded": {"type": "string", "format": "date-time"}
    }
}
