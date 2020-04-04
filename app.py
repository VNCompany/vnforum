import os
from flask import Flask, redirect, send_from_directory, request
import db_session as dbs
import flask_login as fl
from flask_login import login_required, logout_user

from controllers.index_controller import IndexController
from controllers.register_controller import RegisterController
from controllers.login_controller import LoginController
from controllers.information_controller import InformationController
from controllers.category_add_controller import CategoryAddController
from controllers.error404_controller import Error404Controller
from controllers.perm_error_controller import PermErrorController
from controllers.topic_add_controller import TopicAddController

from models.user_model import User

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['SECRET_KEY'] = "yandexlyceum_secret_key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route("/uploads/profiles/<filename>")
def get_profile_uploads(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], "user_avatars"), filename)


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
