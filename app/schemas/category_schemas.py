# JSON schema to validate category creation
category_create_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50,
            "description": "The name of the category, must be unique."
        }
    },
    "required": ["name"]
}
