import datetime
import sqlalchemy as sql
from sqlalchemy import orm
from db_session import SqlAlchemyBase

from models.user_model import User


class Post(SqlAlchemyBase):
    __tablename__ = "posts"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    content = sql.Column(sql.String)
    topic_id = sql.Column(sql.Integer, sql.ForeignKey('topics.id'))
    date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    last_date = sql.Column(sql.DateTime, default=datetime.datetime.now)

    user = orm.relation('User')
    topic = orm.relation('Topic')

    def can_change(self, user: User):
        if user.is_banned():
            return False
        user.id == self.user_id or user.is_admin()

    def can_delete(self, user: User):
        return user.is_admin()
