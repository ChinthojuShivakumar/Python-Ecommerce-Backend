from flask import Flask
from Routes.user_route import auth_bp
from models import initialize_db
from config import Config



app = Flask(__name__)

app.config.from_object(Config)
initialize_db(app)

app.register_blueprint(auth_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5001)