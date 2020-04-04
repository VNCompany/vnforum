from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
import wtforms.validators as valid


class TopicAddForm(FlaskForm):
    title = StringField("Заголовок:",
                        validators=[valid.DataRequired(),
                                    valid.Length(min=1, max=64)])
    tags = StringField("Теги (через зяпятую):",
                       validators=[valid.Length(max=100)])
    is_writeable = BooleanField("Разрешить комментирование:", default=True)
    category = SelectField("Категория:",
                           validators=[valid.DataRequired()])
    content = TextAreaField("Текст:",
                            validators=[valid.Length(min=10, max=9700)])
