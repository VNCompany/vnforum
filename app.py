from flask import Flask
import db_session as dbs

from controllers.index_controller import IndexController


app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"


@app.route("/")
@app.route("/index")
def index():
    controller = IndexController()
    return controller.view()


if __name__ == '__main__':
    dbs.global_init("db/database.sqlite")
    app.run(host="127.0.0.1", port=5000)
