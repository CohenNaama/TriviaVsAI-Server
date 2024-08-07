# JSON schema to validate the creation of a new role
create_role_schema = {
    "type": "object",
    "properties": {
        "role_name": {"type": "string"}
    },
    "required": ["role_name"]
}