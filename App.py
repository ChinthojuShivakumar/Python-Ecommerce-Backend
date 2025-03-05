from flask import Flask, request, jsonify
from Routes.user_route import auth_bp
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

app.register_blueprint(auth_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5001)