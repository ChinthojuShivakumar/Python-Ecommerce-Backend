from flask import Blueprint
from Controllers.user_controller import register, login, get_users_list

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    return register()

@auth_bp.route("/login", methods=["POST"])
def login_user():
    return login()

@auth_bp.route("/user", methods=["GET"])
def fetch_users():
    return get_users_list()