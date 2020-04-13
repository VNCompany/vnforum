import os
import json
from flask import Flask, redirect, send_from_directory, request, abort
import db_session as dbs
import flask_login as fl
from flask_login import login_required, logout_user

from components.db_worker import DataBaseWorker
from components.db_worker import DbwEditTopic

from __imports import *

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['SECRET_KEY'] = "yandexlyceum_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_SIZE'] = 1024 * 1024 * 8

login_manager = fl.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = dbs.create_session()
    return session.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    controller = IndexController()
    return controller.view(dbs.create_session())


@app.route("/register", methods=['GET', 'POST'])
def register():
    if fl.current_user.is_authenticated:
        return redirect("/")
    controller = RegisterController()
    return controller.view(dbs.create_session())


@app.route("/login", methods=['GET', 'POST'])
def login():
    if fl.current_user.is_authenticated:
        return redirect("/")
    controller = LoginController()
    return controller.view(dbs.create_session())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/information")
@login_required
def information():
    controller = InformationController()
    return controller.view()


@app.route("/admin/category_add", methods=['GET', 'POST'])
def category_add():
    if not fl.current_user.is_authenticated or not fl.current_user.is_admin():
        return perm_error()
    controller = CategoryAddController()
    return controller.view(dbs.create_session())


@app.route("/topic_add", methods=['GET', 'POST'])
def topic_add():
    if not fl.current_user.is_authenticated:
        return perm_error(error="Чтобы добавить тему, вы должны быть авторизованы.")
    if fl.current_user.is_banned():
        return perm_error(error="Ваш аккаунт заблокирован.")
    controller = TopicAddController()
    if "category" in request.args.keys():
        return controller.view(dbs.create_session(), category=request.args['category'])
    else:
        return controller.view(dbs.create_session())


@app.route("/topic/<int:topic_id>/edit", methods=['GET', 'POST'])
@login_required
def topic_edit(topic_id: int):
    dbw = DbwEditTopic(dbs.create_session(), topic_id, fl.current_user)
    status = dbw.check()
    if status[0] == "ok":
        controller = TopicEditController(dbw)
        return controller.view()
    elif status[0] == "404_error":
        abort(404)
    else:
        return PermErrorController().view(error=status[1])


@app.route("/category/<int:cat_id>", methods=['GET'])
def get_topics(cat_id: int):
    session = dbs.create_session()
    cat = session.query(Category).get(cat_id)
    if not cat:
        abort(404)
    controller = TopicsController(cat)
    page = 1
    if "page" in request.args.keys():
        page = int(request.args['page'])
    return controller.view(session, page)


@app.route("/topic/<int:topic_id>")
def get_posts(topic_id: int):
    controller = TopicController(dbs.create_session(), topic_id)
    page = 1
    if "page" in request.args.keys():
        page = int(request.args['page'])
    return controller.view(page)


@app.route("/topic/<int:topic_id>/close")
@fl.login_required
def close_topic(topic_id: int):
    session = dbs.create_session()
    topic = session.query(Topic).get(topic_id)
    if topic:
        if topic.can_close(fl.current_user):
            topic.is_closed = True
            session.add(topic)
            session.commit()
            return redirect("/topic/" + str(topic_id))
        else:
            return PermErrorController().view(error="Не удалось закрыть тему")
    else:
        abort(404)


@app.route("/uploads/profiles/<filename>")
def get_profile_uploads(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], "user_avatars"), filename)


@app.route("/ajax/vote", methods=['POST'])
def vote():
    if not fl.current_user.is_authenticated:
        return json.dumps({
            "status": "error",
            "message": "Чтобы голосовать, вы должны быть авторизованы"
        })
    if "value" not in request.form.keys() or \
            "uid" not in request.form.keys() or \
            "type" not in request.form.keys():
        return json.dumps({
            "status": "error",
            "message": "Неверный запрос"
        })
    try:
        uid = int(request.form['uid'])
    except Exception:
        return json.dumps({
            "status": "error",
            "message": "Неверный запрос"
        })
    value = 1 if request.form['value'] == "plus" else -1
    if request.form['type'] == "vote_user":
        status = DataBaseWorker.vote_user(dbs.create_session(), uid, value)
    else:
        status = DataBaseWorker.vote_post(dbs.create_session(), uid, value)
    if status != "error":
        return json.dumps({
            "status": "ok",
            "value": status
        })
    else:
        return json.dumps({
            "status": "error",
            "message": "Не удалось проголосовать"
        })


@app.route("/ajax/topic/<int:topic_id>/add_post", methods=['POST'])
def post_add(topic_id: int):
    err = "Ошибка. Не удалось отправить сообщение."
    if not fl.current_user.is_authenticated:
        return err
    if not request.form.get("content", None) or len(str(request.form['content']).replace(" ", "")) == 0:
        return err
    if DataBaseWorker.add_post(dbs.create_session(), fl.current_user, topic_id, request.form['content']):
        return "ok"
    else:
        return err


@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
def post_edit(post_id: int):
    controller = PostEditorController(dbs.create_session(), post_id)
    return controller.view()


@app.route("/post/<int:post_id>/delete")
@login_required
def post_delete(post_id: int):
    if not fl.current_user.is_admin():
        return "You're not administrator"
    session = dbs.create_session()
    post = session.query(Post).get(post_id)
    if post:
        session.delete(post)
        session.commit()
        return "ok"
    else:
        return "The post doesn't exist"


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    controller = ProfileController(dbs.create_session())
    return controller.view()


@app.route("/topic/<int:topic_id>/delete")
@login_required
def topic_delete(topic_id: int):
    if not fl.current_user.is_admin():
        return "You're not administrator"
    session = dbs.create_session()
    topic = session.query(Topic).get(topic_id)
    if not topic:
        return "The topic doesn't exists"
    session.query(Post).filter(Post.topic_id == topic_id).delete()
    session.commit()
    session.delete(topic)
    session.commit()
    return "ok"


@app.route("/profile/user_edit", methods=['POST'])
def user_edit():
    user = fl.current_user
    if not user.is_authenticated:
        return "Ваша сессия истекла"
    data = request.form
    if "type" not in data.keys():
        return "Неверный запрос"

    if data['type'] == "user_change_password":
        if not data.get('opw', None) or not data.get('npw', None):
            return "Неверный запрос"
        elif not user.check_password(data['opw']):
            return "Неверный старый пароль"
        else:
            session = dbs.create_session()
            guser = session.query(User).get(user.id)
            guser.set_password(data['npw'])
            session.add(guser)
            session.commit()
            logout_user()
            return "ok"
    elif data['type'] == "user_change_email":
        if not data.get('email', None):
            return "Неверный запрос"
        if user.email == data['email']:
            return "Email совпадает со старым"
        session = dbs.create_session()
        guser = session.query(User).get(user.id)
        guser.email = data['email']
        session.add(guser)
        session.commit()
        return "ok"
    elif data['type'] == "user_change_nickname":
        if not data.get('nickname', None):
            return "Неверный запрос"
        if user.nickname == data['nickname']:
            return "Никнейм совпадает со старым"
        if len(user.nickname) > 25:
            return "Никнейм слишком длинный"
        session = dbs.create_session()
        guser = session.query(User).get(user.id)
        guser.nickname = data['nickname']
        session.add(guser)
        session.commit()
        return "ok"


@app.route("/user/<int:user_id>")
@fl.login_required
def get_user_info(user_id: int):
    if fl.current_user.is_banned():
        return PermErrorController().view(error="Вы заблокированы. Доступ к данному ресурсу запрещён")
    else:
        return UserInfoController(dbs.create_session(), user_id).view()


def perm_error(error=""):
    controller = PermErrorController()
    return controller.view(error=error)


@app.errorhandler(404)
def error404(e):
    controller = Error404Controller()
    return controller.view()


@app.route("/search", methods=['GET', 'POST'])
def search():
    controller = SearchController()
    return controller.view()


if __name__ == '__main__':
    dbs.global_init("db/database.sqlite")
    app.run(host="127.0.0.1", port=80)
