import sqlalchemy as sql
from sqlalchemy.orm import Session

from models.user_model import User


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
