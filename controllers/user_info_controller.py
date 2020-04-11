from .__imports import *

from sqlalchemy.orm import Session
from models.user_model import User


class UserInfoController(Controller):
    __view__ = "user_info"
    __title__ = "%USER%"

    def __init__(self, session: Session, user_id: int):
        super(UserInfoController, self).__init__()
        self.css("user_info.css")
        self.javascript("user_info.js")
        self.session = session
        self.user_id = user_id

    def view(self, **kwargs):
        user = self.session.query(User).get(self.user_id)

        if not user:
            abort(404)
        else:
            self.__title__ = user.nickname
            return super(UserInfoController, self).view(user=user)
