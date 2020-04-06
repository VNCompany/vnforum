from .__imports import *
from forms.topic_add_form import TopicAddForm
from components.sc_man import short_code_parser

from sqlalchemy.orm import Session
from models.topic_model import Topic
from models.post_model import Post
from models.user_model import User
from models.category_model import Category


class TopicAddController(Controller):
    __view__ = "topic_add"
    __title__ = "Новая тема"

    def __init__(self):
        super(TopicAddController, self).__init__()
        self.css("custom_form.css")
        self.javascript("topic_add.js")
        self.form = TopicAddForm()

    def view(self, session: Session, **kwargs):
        choices = []

        for cat in session.query(Category).all():
            choices.append(("cat-" + str(cat.id), cat.title))

        self.form.category.choices = choices

        if kwargs.get('category', None):
            self.form.category.data = "cat-" + str(kwargs['category'])
            self.form.category.render_kw = {
                "disabled": True
            }

        if self.form.validate_on_submit():
            content = short_code_parser(self.form.content.data)
            sel_cat = int(self.form.category.data.split("-")[1])
            topic = Topic(
                user_id=current_user.id,
                category_id=sel_cat,
                title=self.form.title.data,
                tags=self.form.tags.data,
                is_writeable=self.form.is_writeable.data
            )
            post = Post(
                user_id=current_user.id,
                content=content,
            )
            DataBaseWorker.add_topic(session, topic, post)
            return redirect("/category/" + str(sel_cat))
        else:
            return super(TopicAddController, self).view(form=self.form)
