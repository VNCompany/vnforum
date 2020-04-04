from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
import wtforms.validators as valid


class CategoryAddForm(FlaskForm):
    title = StringField("Заголовок:",
                        validators=[valid.DataRequired(),
                                    valid.Length(min=1, max=64)])
    description = TextAreaField("Описание:",
                                validators=[valid.Length(max=300)])
    icon = StringField("Класс иконки:", default="fa-c-default")
