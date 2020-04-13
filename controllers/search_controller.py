from .__imports import *

from models.topic_model import Topic
import re


class SearchController(Controller):
    __view__ = "search"
    __title__ = "Поиск"

    def __init__(self):
        super(SearchController, self).__init__()
        self.css("topics.css")
        self.page = 1

    def view(self, **kwargs):
        if "page" in request.args.keys():
            self.page = int(request.args['page'])
        if "text" in request.args.keys() or "tag" in request.args.keys():
            self.view_values()
            return super(SearchController, self).view()
        else:
            return "fail"

    def view_values(self):
        self.__title__ = "Результаты поиска"
        self.__view__ = "search_values"
        if "text" in request.args.keys():
            pages = DataBaseWorker.search_topic(self.db_session, request.args['text'], self.page, 1)
        elif "tag" in request.args.keys():
            pages = DataBaseWorker.search_topic(self.db_session, request.args['tag'], self.page, 0)
        else:
            pages = None

        if pages:
            self.view_includes['topics'] = pages[0]
            self.pagination(pages[1], self.page, self.page_link())
        else:
            self.view_includes['topics'] = []

    @staticmethod
    def page_link():
        url = request.url
        url = re.sub(r"&page=[0-9]+", "", url)
        if "?" in url:
            url += "&page=%id"
        else:
            url += "?page=%id"
        return url
