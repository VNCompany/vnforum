from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField
import wtforms.validators as val


class TopicEditForm(FlaskForm):
    cat_id = SelectField()
    title = StringField(validators=[val.DataRequired()])
    tags = StringField()
    is_writeable = BooleanField()
    is_closed = BooleanField()
