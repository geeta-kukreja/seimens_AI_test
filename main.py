# app.py
import os
import logging
from flask import Flask
from dotenv import load_dotenv
from app.chat_routes import chat_api
from app.auth_routes import auth_api
from config import SECRET_KEY

load_dotenv()
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(chat_api)
app.register_blueprint(auth_api)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


@app.route("/")
def index():
    return "Welcome to the Conversational AI Service!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    from db_connection import set_up_db
    set_up_db()
    app.run(host="0.0.0.0", port=port, debug=True)
