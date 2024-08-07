"""
Utility functions for various common operations.

This module provides helper functions used across different parts of
the application, such as file handling and permission checks.
"""

import os
from app.models.user import User
import logging
from werkzeug.utils import secure_filename
from app.config import Config

logger = logging.getLogger(__name__)


def is_admin(user_id):
    """
    Check if the user is an admin.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    user = User.query.filter_by(id=user_id).first()

    if user.role_id == 1:
        return True
    else:
        logger.log(level=40, msg="Permission denied from is_admin. Admin only!")
        return


def allowed_file(filename):
    """
    Check if the file is allowed based on its extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_profile_picture(file):
    """
    Save the profile picture to the upload directory.

    Args:
        file (FileStorage): The uploaded file.

    Returns:
        str: The filename if the file is saved, None otherwise.
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        return filename
    return None
