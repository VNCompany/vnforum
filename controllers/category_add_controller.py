from .__imports import *

from forms.category_add_form import CategoryAddForm
from models.category_model import Category


class CategoryAddController(Controller):
    __view__ = "category_add"
    __title__ = "Новая категория"

    def __init__(self):
        super(CategoryAddController, self).__init__()
        self.form = CategoryAddForm()
        self.css("custom_form.css")

    def view(self, session, **kwargs):
        if self.form.validate_on_submit():
            category = Category(
                title=self.form.title.data,
                description=self.form.description.data,
                icon=self.form.icon.data
            )
            status = DataBaseWorker.add_category(session, category)
            if status == "ok":
                return redirect("/")
        else:
            return super(CategoryAddController, self).view(form=self.form)
