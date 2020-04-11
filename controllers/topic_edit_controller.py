from .__imports import *

from forms.topic_edit_form import TopicEditForm
from components.db_worker import DbwEditTopic
from models.category_model import Category


class TopicEditController(Controller):
    __view__ = "topic_edit"
    __title__ = "Редактирование темы"

    def __init__(self, dbw: DbwEditTopic):
        super(TopicEditController, self).__init__()
        self.css("custom_form.css")
        self.form = TopicEditForm()
        self.dbw = dbw

    def view(self, **kwargs):
        self.form.cat_id.choices = self.dbw.get_cat_choices()
        if self.form.validate_on_submit():
            if self.dbw.update_topic(
                cat_id=int(self.form.cat_id.data),
                title=self.form.title.data,
                tags=self.form.tags.data,
                is_w=self.form.is_writeable.data,
                is_c=self.form.is_closed.data
            ) == "ok":
                return redirect(self.dbw.redirect_to())
            else:
                return super(TopicEditController, self).view(form=self.form,
                                                             cat_choices=self.form.cat_id.choices,
                                                             topic=self.dbw.get_topic())
        else:
            return super(TopicEditController, self).view(form=self.form,
                                                         cat_choices=self.form.cat_id.choices,
                                                         topic=self.dbw.get_topic())
