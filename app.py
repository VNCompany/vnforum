from flask import Flask, redirect
import db_session as dbs
import flask_login as fl
from flask_login import login_required, logout_user

from controllers.index_controller import IndexController
from controllers.register_controller import RegisterController
from controllers.login_controller import LoginController

from models.user_model import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"
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
    return controller.view()


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


if __name__ == '__main__':
    dbs.global_init("db/database.sqlite")
    app.run(host="127.0.0.1", port=5000)
