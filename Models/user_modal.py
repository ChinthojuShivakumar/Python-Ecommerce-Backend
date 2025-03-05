from models import mongo
import datetime

class User:
    def __init__(self, name, email, password, confirm_password, phone, role):
        self.name = name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.phone = phone
        self.created_at = datetime.datetime.utcnow()  # Set created timestamp
        self.updated_at = datetime.datetime.utcnow()  # Set updated timestamp initially same as created
        self.deleted_at = None  # Default None (not deleted)
        self.deleted = False
        self.role = role
        

    def to_dict(self):
         return {
            "name": self.name, 
            "email": self.email, 
            "password": self.password, 
            "confirm_password": self.confirm_password, 
            "phone": self.phone,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at,
            "deleted": self.deleted
        }
    
    def save_to_db(self):
        result =  mongo.db.users.insert_one(self.to_dict()).inserted_id
        return str(result)
    
    def update_user_timestamp(self, update_data):
        update_data["updated_at"] = datetime.datetime.utcnow()
        result =  mongo.db.users.update_one({"email": self.email}, {"$set": update_data})
        return str(result)
    
    def delete_user_timestamp(self):
       result =  mongo.db.users.update_one({'email': self.email, "$set": {"deleted_at": datetime.datetime.utcnow(), "deleted": True}})
       return str(result)

   