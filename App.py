from flask import Flask, request, jsonify
from Routes.user_route import auth_bp
from Routes.product_route import product_bp
from models import initialize_db
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
initialize_db(app)

@app.before_request
def check_auth():
    
    open_routes = ["/api/register", "/api/login"]
    if request.path not in open_routes:
        auth_headers = request.headers.get("Authorization")
        if not auth_headers:
            return jsonify({"message": "unauthorized"}), 401
        
def populate(lookup_collection, local_field, foreign_field, alias):
    return [
        {
            "$lookup" : {
                "from": lookup_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": alias
            }  
        },
        {"$unwind": f"${alias}"}
    ]


app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(product_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5001)