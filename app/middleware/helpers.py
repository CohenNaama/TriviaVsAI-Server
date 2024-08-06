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
