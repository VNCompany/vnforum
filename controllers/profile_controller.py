from .__imports import *
import os

from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from models.user_model import User


class ProfileController(Controller):
    __view__ = "profile"
    __title__ = "Профиль"
    MAX_IMAGE_SIZE = 1024 * 1024 + 1

    def __init__(self, session: Session):
        super(ProfileController, self).__init__()
        self.css("profile.css")
        self.session = session

    def view(self, **kwargs):
        if request.method == 'GET':
            return super(ProfileController, self).view(user=current_user)
        else:
            user_avatar = request.files['user_avatar']
            if user_avatar.filename and len(user_avatar.filename.split('.')) > 1:
                extension = user_avatar.filename.split('.')[-1]
                fn = str(current_user.id) + "." + extension
                fn = secure_filename(fn)
                data = user_avatar.read(self.MAX_IMAGE_SIZE)
                if len(data) != self.MAX_IMAGE_SIZE:
                    abs_path = "./uploads/user_avatars/" + fn
                    # if os.path.exists(abs_path):
                    #     os.remove(abs_path)
                    with open(abs_path, mode="wb") as ava:
                        ava.write(data)
                    user = self.session.query(User).get(current_user.id)
                    if user:
                        user.avatar = fn
                        self.session.add(user)
                        self.session.commit()
                        current_user.avatar = fn
                        return super(ProfileController, self).view(user=current_user)
                    else:
                        return super(ProfileController, self).view(user=current_user,
                                                                   error="Ваша сессия истекла. Перезагрузите страницу")
                else:
                    return super(ProfileController, self).view(user=current_user,
                                                               error="Размер файла не должен превышать 1 МБ")
            else:
                return super(ProfileController, self).view(user=current_user, error="Неверный формат имени")
