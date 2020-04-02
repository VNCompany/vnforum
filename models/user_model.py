import datetime
import sqlalchemy as sql
from db_session import SqlAlchemyBase

# Statuses:
# 0 - not_authenticated
# 1 - user
# 2 - admin
# 3 - banned


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    login = sql.Column(sql.String, unique=True, nullable=False)
    password = sql.Column(sql.String, nullable=False)
    email = sql.Column(sql.String, nullable=False, unique=True)
    nickname = sql.Column(sql.String, nullable=False, unique=True)
    status = sql.Column(sql.Integer, nullable=False, default=1)
