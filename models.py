from flask_pymongo import PyMongo

mongo = PyMongo()

def initialize_db(app):
    mongo.init_app(app)

    db = mongo.db
    required_collections = ["users", "products", "orders"]

    for collection in required_collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)

    