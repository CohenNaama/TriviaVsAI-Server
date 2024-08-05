import os
from app.models.user import User
import logging
from werkzeug.utils import secure_filename
from app.config import Config

logger = logging.getLogger(__name__)


def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user.role_id == 1:
        return True
    else:
        logger.log(level=40, msg="Permission denied from is_admin. Admin only!")
        return


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_profile_picture(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        return filename
    return None


login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"]
}

create_role_schema = {
    "type": "object",
    "properties": {
        "role_name": {"type": "string"}
    },
    "required": ["role_name"]
}

user_create_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "profile_picture": {"type": "string", "default": "default.jpg"},
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
