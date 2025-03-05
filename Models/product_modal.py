import datetime
from models import mongo

class Product:
    def __init__(self, name, price, category, stock, image_url=None):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock
        self.image_url = image_url
        self.created_at = datetime.datetime.utcnow()  # Set created timestamp
        self.updated_at = datetime.datetime.utcnow()  # Set updated timestamp initially same as created
        self.deleted_at = None  # Default None (not deleted)
        self.deleted = False


    def to_dict(self):
        return {
            "name": self.name,
            "price":self.price,
            "category": self.category,
            "stock": self.category,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at,
            "deleted": self.deleted
        }
    

    def save_to_db(self):
        result = mongo.db.products.insert_one(self.to_dict()).inserted_id
        return str(result)