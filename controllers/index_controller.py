from .__imports import *

from sqlalchemy.orm import Session
from models.category_model import Category


class IndexController(Controller):
    __view__ = "index"
    __title__ = "Главная страница"

    def __init__(self):
        super(IndexController, self).__init__()
        self.css("index.css", "category_icons.css")

    def view(self, session: Session, **kwargs):
        cats = session.query(Category).all()
        return super(IndexController, self).view(cats=cats)
