import os
import datetime
from models import mongo
from config import Config
from bson.objectid import ObjectId
from Models.product_modal import Product
from flask import jsonify


def get_all_product_list():
    try: 
        product_list = list(mongo.db.products.find({"deleted": False}))
        for product in product_list:
            product["_id"] = str(product["_id"])
        return jsonify({"message":"Products List Fetched successfully", "products_list": product_list}), 200
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

