from .__imports import *

from models.category_model import Category


class TopicsController(Controller):
    __view__ = "topics"

    def __init__(self, category: Category):
        self.cat = category
        self.__title__ = self.cat.title
        super(TopicsController, self).__init__()
        self.css("topics.css")
