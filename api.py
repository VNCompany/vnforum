import flask
from datetime import datetime
from flask import request, jsonify

from db_session import create_session
from sqlalchemy.orm import Session

from models.user_model import User
from models.topic_model import Topic

blueprint = flask.Blueprint("api", __name__,
                            template_folder="templates")


@blueprint.route("/api/token_get", methods=['POST'])
def api_token_get():
    data = request.get_json(silent=True, force=True)
    response = {"status": "error"}
    if not data or type(data).__name__ != "dict":
        response['message'] = "invalid request"
        return jsonify(response)
    if "login" not in data or "password" not in data:
        response['message'] = "invalid login or password"
        return jsonify(response)
    u_login = data.get("login")
    u_pw = data["password"]
    session = create_session()
    user = session.query(User).filter(User.login == u_login).first()
    if not user or not user.check_password(u_pw):
        response['message'] = "invalid login or password"
        return jsonify(response)
    else:
        response['status'] = "ok"
        response['api_key'] = user.token
        return jsonify(response)


@blueprint.route("/api/user_get/", methods=['GET'])
def api_user_get():
    def error(msg: str):
        return jsonify({
            "status": "error",
            "message": msg
        })
    if "api_key" not in request.args:
        return error("invalid api key")
    session = create_session()
    user = api_key_check(request.args['api_key'], session)
    if not user:
        return error("invalid api key")
    if "nickname" not in request.args:
        return error("nickname not specified")
    f_user = session.query(User).filter(User.nickname == request.args['nickname']).first()
    if not f_user:
        return error("user not found")
    return jsonify({
        "status": "ok",
        "user": {
            "id": f_user.id,
            "sex": f_user.sex,
            "email": f_user.email,
            "nickname": f_user.nickname,
            "register_date": f_user.reg_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "avatar": request.url_root + "uploads/profiles/" + f_user.avatar,
            "rating": f_user.rating
        }
    })


@blueprint.route("/api/topic_info_get/", methods=['GET'])
def api_topic_info_get():
    def error(msg: str):
        return jsonify({
            "status": "error",
            "message": msg
        })
    if "api_key" not in request.args:
        return error("invalid api key")
    session = create_session()
    user = api_key_check(request.args['api_key'], session)
    if not user:
        return error("invalid api key")

    if "topic_id" not in request.args:
        return error("topic id not specified")
    try:
        topic_id = int(request.args['topic_id'])
        topic = session.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return error("topic not found")
        return jsonify({
            "status": "ok",
            "topic": {
                "id": topic.id,
                "user": {
                    "id": topic.user.id,
                    "nickname": topic.user.nickname,
                    "rating": topic.user.rating
                },
                "title": topic.title,
                "category": {
                    "id": topic.category_id,
                    "title": topic.category.title
                },
                "tags": topic.tags,
                "date": topic.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "is_writable": topic.is_writeable,
                "is_closed": topic.is_closed,
                "last_post": topic.get_last_post().date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        })
    except TypeError:
        return error("invalid topic id")


def api_key_check(token: str, session: Session) -> User:
    user = session.query(User).filter(User.token == token).first()
    return user
