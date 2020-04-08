import os
import json
from flask import Flask, redirect, send_from_directory, request, abort
import db_session as dbs
import flask_login as fl
from flask_login import login_required, logout_user
from components.db_worker import DataBaseWorker

from controllers.index_controller import IndexController
from controllers.register_controller import RegisterController
from controllers.login_controller import LoginController
from controllers.information_controller import InformationController
from controllers.category_add_controller import CategoryAddController
from controllers.error404_controller import Error404Controller
from controllers.perm_error_controller import PermErrorController
from controllers.topic_add_controller import TopicAddController
from controllers.topics_controller import TopicsController
from controllers.topic_controller import TopicController

from models.user_model import User
from models.category_model import Category
from models.topic_model import Topic
from models.post_model import Post

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['SECRET_KEY'] = "yandexlyceum_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PAGE_COUNT = 20

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
    controller = TopicController()
    return controller.view()


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


def perm_error(error=""):
    controller = PermErrorController()
    return controller.view(error=error)


@app.errorhandler(404)
def error404(e):
    controller = Error404Controller()
    return controller.view()


if __name__ == '__main__':
    dbs.global_init("db/database.sqlite")
    app.run(host="127.0.0.1", port=80)
