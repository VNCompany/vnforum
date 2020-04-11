from .__imports import *

from sqlalchemy.orm import Session

from models.topic_model import Topic
from components.sc_man import short_code_parser
import base64


class TopicController(Controller):
    __view__ = "topic"
    __title__ = "Title"

    def __init__(self, session: Session, topic_id: int):
        super(TopicController, self).__init__()
        self.css("topic.css")
        self.css("code.css")
        self.css("vneditor/vneditor.css")
        self.javascript("topic.js")
        self.javascript("rainbow-custom.min.js")
        self.javascript("vneditor/vneditor.js")
        self.session = session
        self.topic = session.query(Topic).get(topic_id)
        if not self.topic:
            abort(404)
        self.session = session
        self.__title__ = self.topic.short_title(30)

    def view(self, page: int, **kwargs):
        opage = DataBaseWorker.get_topics(self.session, self.topic.id, page, False)
        if opage is None:
            abort(404)
        else:
            self.pagination(opage[1], page, "?page=%id")
            self.view_includes['posts'] = opage[0]
            self.view_includes['topic'] = self.topic
            self.view_includes['generate_content'] = short_code_parser
            self.view_includes['page_number'] = page
            self.view_includes['generate_edit_link'] = self.gen_link
            return super(TopicController, self).view(**kwargs)

    @staticmethod
    def gen_link(post_id, page, post_index):
        value = base64.b64encode(bytes(str(page) + " " + str(post_index), encoding="utf-8"))
        return "/post/" + str(post_id) + "/edit?link=" + value.decode("utf-8")
