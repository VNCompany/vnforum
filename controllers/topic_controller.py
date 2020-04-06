from .__imports import *

from sqlalchemy.orm import Session

from models.topic_model import Topic


class TopicController(Controller):
    __view__ = "topic"
    __title__ = "Title"

    def __init__(self):
        super(TopicController, self).__init__()
        self.css("topic.css")
        # topic = session.query(Topic).get(topic_id)
        # if not topic:
        #     abort(404)
        # self.session = session
