import re
from sqlalchemy.orm import Session
from flask_login import current_user

from .pagination import html_pagination, get_page, POSTS_PAGE_LENGTH, TOPICS_PAGE_LENGTH

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

    @staticmethod
    def get_topics(session: Session, cat_id: int, page: int):
        ids = session.query(Topic.id).filter(Topic.category_id == cat_id).order_by(Topic.id.desc()).all()
        ids = [i[0] for i in ids]
        result = get_page(ids, page, TOPICS_PAGE_LENGTH)
        if result is None:
            return None
        else:
            items = session.query(Topic).filter(Topic.id.in_(result[0])).all()
            return items, result[1]

    @staticmethod
    def vote_user(session: Session, user_id: int, count: int):
        if not current_user.is_authenticated:
            return "error"
        user = session.query(User).get(user_id)
        if user:
            user.vote(current_user.id, count)
            session.commit()
            return user.rating
        else:
            return "error"

    @staticmethod
    def vote_post(session: Session, post_id: int, count: int):
        if not current_user.is_authenticated:
            return "error"
        post = session.query(Post).get(post_id)
        if post:
            post.vote(current_user.id, count)
            session.commit()
            return post.rating
        else:
            return "error"
