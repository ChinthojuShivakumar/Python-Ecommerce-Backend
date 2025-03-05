from flask import Blueprint
from Controllers.user_controller import register, login, get_users_list, update_user,delete_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    return register()

@auth_bp.route("/login", methods=["POST"])
def login_user():
    return login()

# @auth_bp.route("/user", methods=["POST"])
# def register_user():
#     return register()


@auth_bp.route("/user", methods=["GET"])
def fetch_users():
    return get_users_list()

@auth_bp.route("/user/<user_id>", methods=["PATCH"])
def edit_user(user_id):
    return update_user(user_id=user_id)

@auth_bp.route("/user/<user_id>", methods=["DELETE"])
def remove_user(user_id):
    return delete_user(user_id=user_id)