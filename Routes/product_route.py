from flask import Blueprint
from Controllers.product_controller import get_all_product_list

product_bp = Blueprint("Products", __name__)

@product_bp.route("/product", methods=["GET"])
def fetch_product():
    return get_all_product_list()