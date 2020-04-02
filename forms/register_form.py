from flask_wtf import FlaskForm
from wtforms import PasswordField, RadioField, StringField
from wtforms.fields.html5 import EmailField
import wtforms.validators as validate


class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[validate.DataRequired()])
    login = StringField("Логин (нужен для авторизации): ", validators=[validate.DataRequired(),
                                                                       validate.Length(min=4, max=100)])
    password = PasswordField("Пароль: ", validators=[validate.DataRequired(),
                                                     validate.Length(min=8, max=64),
                                                     validate.EqualTo("confirm", "Пароли не совпадают")])
    confirm = PasswordField("Повтор:", validators=[validate.DataRequired()])
    nickname = StringField("Никнейм: ", validators=[validate.DataRequired(),
                                                    validate.Length(max=25)])
    sex = RadioField("Выберите пол: ", choices=[("male", "Мужской"), ("female", "Женский")], default="male")
