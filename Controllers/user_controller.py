from flask import request, jsonify
from models import mongo
from Models.user_modal import User
from bson.objectid import ObjectId
import jwt
import datetime
from config import Config
import traceback
from bson import ObjectId

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
        user_list = list(mongo.db.users.find({"deleted": False}, {"deleted": 0, "deleted_at": 0}))
        for user in user_list:
            user["_id"] = str(user["_id"]) 
        return jsonify({"message":"Users List Fetched successfully", "user_list": user_list}), 200
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

def update_user(user_id):
    try:
        data = request.json
        find_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not find_user:
            return jsonify({"message":"User not found", "find_user": find_user}), 400
        find_user["updated_at"] = datetime.datetime.utcnow()
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        updated_user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"deleted": 0, "deleted_at": 0})
        if updated_user:
            updated_user["_id"] = str(updated_user["_id"])
        return jsonify({"message": "user updated successfully", "user": updated_user}), 202
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
    
def delete_user(user_id):
    try:
        data = request.json
        find_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not find_user:
            return jsonify({"message":"User not found", "find_user": find_user}), 400
        find_user["updated_at"] = datetime.datetime.utcnow()
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"deleted": True, "deleted_at":datetime.datetime.utcnow()}})
        deleted_user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"deleted": 0, "deleted_at": 0})
        if deleted_user:
            deleted_user["_id"] = str(deleted_user["_id"])
        return jsonify({"message": "user deleted successfully", "user": deleted_user}), 202
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


