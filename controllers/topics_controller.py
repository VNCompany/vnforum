from .__imports import *

from sqlalchemy.orm import Session

from models.category_model import Category


class TopicsController(Controller):
    __view__ = "topics"

    def __init__(self, category: Category):
        self.cat = category
        self.__title__ = self.cat.title
        super(TopicsController, self).__init__()
        self.css("topics.css")
        self.view_includes["cat"] = self.cat

    def view(self, session: Session, page: int, **kwargs):
        opage = DataBaseWorker.get_topics(session, self.cat.id, page)
        if opage is None:
            self.view_includes['topics'] = []
            return super(TopicsController, self).view(**kwargs)
        else:
            self.pagination(opage[1], page, "?page=%id")
            self.view_includes['topics'] = opage[0]
            return super(TopicsController, self).view(**kwargs)
