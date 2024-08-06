login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"]
}

user_create_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "profile_picture": {"type": ["string", "null"], "default": "default.jpg"},
        "level": {"type": "integer", "default": 1},
        "experience_points": {"type": "integer", "default": 0},
    },
    "required": ["username", "email", "password"]
}

user_update_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "profile_picture": {"type": "string"},
        "level": {"type": "integer"},
        "experience_points": {"type": "integer"},
    },
    "required": []
}
