import re
from sqlalchemy.orm import Session
from flask_login import current_user

from components.pagination import get_page, POSTS_PAGE_LENGTH, TOPICS_PAGE_LENGTH

from models.user_model import User
from models.topic_model import Topic
from models.category_model import Category
from models.post_model import Post

from werkzeug.urls import url_encode


class DataBaseWorker:
    re_login = r"^[0-9A-Za-z-_]+$"
    re_nickname = r"^[0-9A-Za-z-_А-Яа-я]+$"
    re_title = r"^[^><]+$"

    @staticmethod
    def add_user(session: Session, user: User):
        if not re.match(DataBaseWorker.re_login, user.login):
            return "Ошибка. Допустимые символы логина: цифры, латинские буквы, -, _"
        if not re.match(DataBaseWorker.re_nickname, user.nickname):
            return "Ошибка. Допустимые символы никнейма: цифры, буквы, -, _"
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
        if not re.match(DataBaseWorker.re_title, topic.title):
            return "Ошибка. Тема не может содержать символы < и >."
        session.add(topic)
        session.commit()
        post.topic_id = topic.id
        session.add(post)
        session.commit()
        return "ok"

    @staticmethod
    def get_topics(session: Session, type_id: int, page: int, is_topic=True):
        if is_topic:
            ids = session.query(Topic.id).filter(Topic.category_id == type_id).order_by(Topic.date.desc()).all()
        else:
            ids = session.query(Post.id).filter(Post.topic_id == type_id).all()
        ids = [i[0] for i in ids]
        if is_topic:
            result = get_page(ids, page, TOPICS_PAGE_LENGTH)
        else:
            result = get_page(ids, page, POSTS_PAGE_LENGTH)
        if result is None:
            return None
        else:
            if is_topic:
                items = session.query(Topic).filter(Topic.id.in_(result[0])).order_by(Topic.id.desc()).all()
            else:
                items = session.query(Post).filter(Post.id.in_(result[0])).all()
            return items, result[1]

    @staticmethod
    def search_topic(session: Session, s_value: str, page: int, t: int):
        topics = session.query(Topic).order_by(Topic.date.desc()).all()
        searched = []
        if t == 0:
            for topic in topics:
                if s_value.lower() in topic.tags:
                    searched.append(topic.id)
        else:
            for topic in topics:
                if s_value.lower() == topic.title.lower() or s_value.lower() in topic.title.lower():
                    searched.append(topic.id)
        result = get_page(searched, page, TOPICS_PAGE_LENGTH)
        if result is None:
            return None
        else:
            items = session.query(Topic).filter(Topic.id.in_(result[0])).order_by(Topic.id.desc()).all()
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

    @staticmethod
    def add_post(session: Session, user: User, topic_id: int, content: str):
        topic = session.query(Topic).get(topic_id)
        if topic:
            if topic.can_post(user):
                post = Post(
                    user_id=user.id,
                    topic_id=topic_id,
                    content=content
                )
                session.add(post)
                session.commit()
                return True
            else:
                return False
        else:
            return False


class DbwEditTopic:
    def __init__(self, session: Session, topic_id: int, user: User):
        self.session = session
        self.topic_id = topic_id
        self.user = user
        self.topic = None

    def check(self):
        if not self.user.is_admin():
            return "perm_error", "Только администраторы могут редактировать темы"
        self.topic = self.session.query(Topic).get(self.topic_id)
        if not self.topic:
            return "404_error", ""
        return "ok", ""

    def get_topic(self) -> Topic:
        return self.topic

    def get_cat_choices(self):
        cats = self.session.query(Category).all()
        return [(str(cat.id), cat.title) for cat in cats]

    def update_topic(self, cat_id: int, title: str, tags: str, is_w: bool, is_c: bool):
        if not title or title.strip() == "":
            return "error"
        self.topic.category_id = cat_id
        self.topic.title = title
        self.topic.tags = tags
        self.topic.is_writeable = is_w
        self.topic.is_closed = is_c
        self.session.add(self.topic)
        self.session.commit()
        return "ok"

    def redirect_to(self):
        return "/topic/" + str(self.topic_id)
