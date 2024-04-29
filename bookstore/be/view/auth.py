from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import user

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login", methods=["POST"])
def login():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    terminal = request.json.get("terminal", "")
    u = user.User()
    code, message, token = u.login(
        user_id=user_id, password=password, terminal=terminal
    )
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    u = user.User()
    code, message = u.logout(user_id=user_id, token=token)
    return jsonify({"message": message}), code


@bp_auth.route("/register", methods=["POST"])
def register():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = user.User()
    code, message = u.register(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = user.User()
    code, message = u.unregister(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/password", methods=["POST"])
def change_password():
    user_id = request.json.get("user_id", "")
    old_password = request.json.get("oldPassword", "")
    new_password = request.json.get("newPassword", "")
    u = user.User()
    code, message = u.change_password(
        user_id=user_id, old_password=old_password, new_password=new_password
    )
    return jsonify({"message": message}), code

# 搜索图书的路由
@bp_auth.route("/search_books_global", methods=["GET"])
def search_books_global():
    query = request.args.get("query", "")
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))
    u = user.User()
    code, books = u.search_books_global(query=query, start=start, size=size)
    return jsonify({"books": books}), code

@bp_auth.route("/search_books_in_store", methods=["GET"])
def search_books_in_store():
    store_id = request.args.get("store_id", "")
    query = request.args.get("query", "")
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))
    u = user.User()
    code, books = u.search_books_in_store(store_id=store_id, query=query, start=start, size=size)
    return jsonify({"books": books}), code
