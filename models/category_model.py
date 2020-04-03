import sqlalchemy as sql
from sqlalchemy import orm
from db_session import SqlAlchemyBase

from models.post_model import Post


class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    icon = sql.Column(sql.String)
    title = sql.Column(sql.String)
    description = sql.Column(sql.String)

    topics = orm.relation("Topic", back_populates="category")
