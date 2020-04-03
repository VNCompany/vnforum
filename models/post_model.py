import datetime
import sqlalchemy as sql
from sqlalchemy import orm
from db_session import SqlAlchemyBase

from models.user_model import User


class Post(SqlAlchemyBase):
    __tablename__ = "posts"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    # TODO: Добавить поле с id топика
    title = sql.Column(sql.String)
    date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    last_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    content = sql.Column(sql.String)

    user = orm.relation('User')

    def can_change(self, user: User):
        user.id == self.user_id or user.is_admin()

    def can_delete(self, user: User):
        return user.is_admin()
