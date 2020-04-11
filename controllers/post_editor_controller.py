from .__imports import *

from sqlalchemy.orm import Session
from models.post_model import Post
import datetime

from forms.post_edit_form import PostEditForm

from .perm_error_controller import PermErrorController
import base64


class PostEditorController(Controller):
    __view__ = "post_editor"
    __title__ = "Редактирование сообщения:"

    def __init__(self, session: Session, post_id: int):
        super(PostEditorController, self).__init__()
        self.css("custom_form.css")
        self.css("vneditor/vneditor.css")
        self.javascript("vneditor/vneditor.js")
        self.form = PostEditForm()

        self.session = session
        self.link = None
        if "link" in request.args.keys():
            result = base64.b64decode(request.args['link'])
            result = result.decode("utf-8").split()
            try:
                self.link = {
                    "page": int(result[0]),
                    "post": int(result[1])
                }
            except Exception:
                abort(404)
                return
        self.post = session.query(Post).get(post_id)
        if not self.post:
            abort(404)

    def view(self, **kwargs):
        if not current_user.is_authenticated or not self.post.can_change(current_user):
            return PermErrorController().view(error="Не удалось изменить сообщение")

        self.view_includes['last_content'] = self.post.content
        if self.form.validate_on_submit():
            self.post.content = self.form.editor.data
            self.post.last_date = datetime.datetime.now()
            self.session.add(self.post)
            self.session.commit()
            if self.link:
                return redirect("/topic/" + str(self.post.topic.id) + "?page=" + str(self.link['page'])
                                + "#post-" + str(self.link['post']))
        else:
            return super(PostEditorController, self).view(**kwargs, form=self.form)
