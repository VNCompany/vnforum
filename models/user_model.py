import datetime
import sqlalchemy as sql
from db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

# Statuses:
# 0 - not_authenticated
# 1 - user
# 2 - admin
# 3 - banned


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    login = sql.Column(sql.String, unique=True, nullable=False)
    password = sql.Column(sql.String)
    avatar = sql.Column(sql.String, default="default.jpg")
    email = sql.Column(sql.String, nullable=False, unique=True)
    sex = sql.Column(sql.String, nullable=False)
    nickname = sql.Column(sql.String, nullable=False, unique=True)
    reg_date = sql.Column(sql.DateTime, default=datetime.datetime.now)

    status = sql.Column(sql.Integer, nullable=False, default=1)
    rating = sql.Column(sql.Integer, default=0)
    votes = sql.Column(sql.String, default="")

    def vote(self, user_id: int, value: int):
        if str(user_id) not in self.votes.split(",") and self.id != user_id:
            self.rating += value
            self.votes += ("," if len(self.votes) > 0 else "") + str(user_id)

    def id_admin(self):
        return self.status == 2

    def is_banned(self):
        return self.status == 3

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
