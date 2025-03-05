import os

class Config:
    SECRET_KEY = "1234"
    JWT_SECRET_KEY = '1232'
    MONGO_URI = "mongodb://localhost:27017/ecommerce_db"
    ALLOWED_TYPES = ["png","jpg", "jpeg"],
    DOMAIN_URI = "http://127.0.0.1:5001"

    @staticmethod
    def allowed_files(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_TYPES