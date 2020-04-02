from flask import Flask
import db_session as dbs
from components.db_worker import DataBaseWorker

from controllers.index_controller import IndexController
from controllers.register_controller import RegisterController

from models.user_model import User


app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"


@app.route("/")
@app.route("/index")
def index():
    controller = IndexController()
    return controller.view()


@app.route("/register", methods=['GET', 'POST'])
def register():
    controller = RegisterController()
    return controller.view(dbs.create_session())


if __name__ == '__main__':
    dbs.global_init("db/database.sqlite")
    app.run(host="127.0.0.1", port=5000)
