from flask_wtf import FlaskForm
from wtforms import TextAreaField
import wtforms.validators as valid


class PostEditForm(FlaskForm):
    editor = TextAreaField(validators=[
        valid.DataRequired()
    ])
