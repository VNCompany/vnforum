import datetime
import sqlalchemy as sql
from sqlalchemy import orm
from db_session import SqlAlchemyBase

from models.user_model import User
from models.post_model import Post


class Topic(SqlAlchemyBase):
    __tablename__ = "topics"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    # TODO: Добавить ид категории
    title = sql.Column(sql.String)
    tags = sql.Column(sql.String)
    date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    is_writeable = sql.Column(sql.Boolean, default=True)
    is_closed = sql.Column(sql.Boolean, default=False)

    user = orm.relation("User")
    posts = orm.relation("Post", back_populates="topic")

    def can_change(self, user: User):
        return user.is_admin()

    def can_post(self, user: User):
        if user.is_banned():
            return False
        if self.is_writeable and not self.is_closed:
            return True
        elif not self.is_writeable and self.user_id == user.id and not self.is_closed:
            return True
        else:
            return False
