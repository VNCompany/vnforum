from .__imports import *
import os

from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from models.user_model import User
from models.topic_model import Topic


class ProfileController(Controller):
    __view__ = "profile"
    __title__ = "Профиль"
    MAX_IMAGE_SIZE = 1024 * 1024 + 1

    def __init__(self, session: Session):
        super(ProfileController, self).__init__()
        self.css("profile.css")
        self.session = session

    def view(self, **kwargs):
        if current_user.is_banned():
            return abort(404)
        user_topics = self.session.query(Topic).filter(Topic.user_id == current_user.id)
        user_topics = sorted([(t.id, t.short_title(100), t.date, t.get_last_post().date) for t in user_topics],
                             key=lambda tt: tt[2],
                             reverse=True)
        if request.method == 'GET':
            return super(ProfileController, self).view(user=current_user, topics=user_topics)
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
                        return super(ProfileController, self).view(user=current_user, topics=user_topics)
                    else:
                        return super(ProfileController, self).view(user=current_user,
                                                                   error="Ваша сессия истекла. Перезагрузите страницу",
                                                                   topics=user_topics)
                else:
                    return super(ProfileController, self).view(user=current_user,
                                                               error="Размер файла не должен превышать 1 МБ",
                                                               topics=user_topics)
            else:
                return super(ProfileController, self).view(user=current_user, error="Неверный формат имени",
                                                           topics=user_topics)
