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
    last_date = sql.Column(sql.DateTime)

    rating = sql.Column(sql.Integer, default=0)
    votes = sql.Column(sql.String, default="")

    user = orm.relation('User')
    topic = orm.relation('Topic')

    def can_change(self, user: User):
        if not self.topic.can_post(user):
            return False
        return user.id == self.user_id or user.is_admin()

    def can_delete(self, user: User):
        return user.is_admin()

    def vote(self, user_id: int, count: int):
        str_id = str(user_id)
        if str_id not in self.votes.split(",") and user_id != self.user.id:
            self.rating += count
            self.votes += ("" if self.votes == "" else ",") + str_id
