from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField
import wtforms.validators as validate


class LoginForm(FlaskForm):
    login = StringField("Логин: ", validators=[validate.DataRequired()])
    password = PasswordField("Пароль: ", validators=[validate.DataRequired()])
    remember_me = BooleanField("Запомнить меня")
