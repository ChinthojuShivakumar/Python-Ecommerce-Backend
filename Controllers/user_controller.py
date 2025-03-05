from flask import request, jsonify
from models import mongo
from Models.user_modal import User
from bson.objectid import ObjectId
import jwt
import datetime
from config import Config
import traceback

def register():
    try:
        data = request.json
        print(data)
        is_user_exist = mongo.db.users.find_one({"email": data["email"]})
        if is_user_exist:
            return jsonify({"message": "User registration failed!"}), 500
        user = User(data["name"], data["email"], data["password"], data["confirm_password"], data["phone"], data["role"])
        new_user = user.save_to_db()
        is_newuser = mongo.db.users.find_one({"_id": ObjectId(new_user)})
        if is_newuser:
            is_newuser["_id"] = str(is_newuser["_id"])
            return jsonify({"message": "User registered successfully!", "user": is_newuser}), 201
        else:
            return jsonify({"message": "User registration failed!"}), 500
    except Exception as e: 
        error_details = traceback.format_exc()
        print("Error during registration:", error_details)
    # return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

def login():
    try:
        data = request.json
        is_user_exist = mongo.db.users.find_one({"email": data["email"]})
        if not is_user_exist:
            return jsonify({"message": "Invalid User Name or Password!"}), 401
         
        if  is_user_exist["password"] != data["password"]:
            return jsonify({"message": "Invalid User Name or Password!"}), 401
        is_user_exist["_id"] = str(is_user_exist["_id"])
        token_payload = {
            "user_id": is_user_exist["_id"],
            "email": is_user_exist["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        }
        token = jwt.encode(token_payload, Config.JWT_SECRET_KEY, algorithm="HS256")
        # user = User(data["name"], data["email"], data["password"])
        return jsonify({"message":"Login Successful","token": token, "user": is_user_exist}), 200
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
    

def get_users_list():
    try:
        user_list = mongo.db.users.find({})
        for user in user_list:
            user["_id"] = str(user["_id"])
        return jsonify({"message":"Users List Fetched successfully", "user_list": user_list}), 200
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

