import re
import sqlalchemy as sql
from flask import url_for
from sqlalchemy.orm import Session
from flask_wtf.file import FileStorage
from werkzeug.utils import secure_filename

from models.user_model import User
from models.topic_model import Topic
from models.category_model import Category
from models.post_model import Post


class DataBaseWorker:
    @staticmethod
    def add_user(session: Session, user: User):
        for u in session.query(User).all():
            if u.login == user.login:
                return "Ошибка. Пользователь с таким логином уже существует."
            elif u.email == user.email:
                return "Ошибка. Пользователь с таким email уже существует"
            elif u.nickname == user.nickname:
                return "Ошибка. Пользователь с таким никнеймом уже существует"
        session.add(user)
        session.commit()
        return "ok"

    @staticmethod
    def check_user(session: Session, login: str, pw: str):
        user = session.query(User).filter(User.login == login).first()
        if user:
            if user.check_password(pw):
                if not user.is_banned():
                    return "ok", user
                else:
                    return "Этот аккаунт заблокирован!",
            else:
                return "Неверный логин или пароль.",
        else:
            return "Неверный логин или пароль.",

    @staticmethod
    def generate_file_name(text: str):
        if len(text) > 20:
            text = text[:20]
        li = re.findall(r"[(A-Za-zА-Яа-я0-9-_#)]", text)
        return "".join(li)

    @staticmethod
    def add_category(session: Session, category: Category):
        session.add(category)
        session.commit()
        return "ok"

    @staticmethod
    def add_topic(session: Session, topic: Topic, post: Post):
        session.add(topic)
        session.commit()
        post.topic_id = topic.id
        session.add(post)
        session.commit()
