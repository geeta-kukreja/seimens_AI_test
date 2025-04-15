from flask import Blueprint, request, jsonify, make_response
import logging
import uuid
from db_connection import get_conn


logger = logging.getLogger(__name__)
auth_api = Blueprint('auth_api', __name__)
# conn = get_conn()


def add_user(username, password):
    session_id = str(uuid.uuid4())
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, session_id) VALUES (%s, %s, %s)", (username, password, session_id))
    conn.commit()
    conn.close()
    return session_id


def get_user(username, password):
    # Get session_id from db
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    conn.close()
    print(user)
    print(type(user))
    print(user[3])
    return user[3] # session id is at the last co


@auth_api.route("/signup", methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid credentials"}), 400

    try:
        session_id = add_user(username, password)
    except Exception as e:
        logger.exception(e)
        return jsonify({"error": "Unable to create user due some internal error"}), 400

    response = make_response({"message": "Sign-up successful"})

    response.delete_cookie('session_id')
    response.set_cookie(
        'session_id',
        session_id
    )
    return response


@auth_api.route("/login", methods=["POST"])
def signin():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid credentials"}), 400

    try:
        session_id = get_user(username, password)
    except Exception as e:
        logger.exception(e)
        return jsonify({"error": "Unable to get user due some internal error"}), 400

    response = make_response({"message": "Sign-in successful"})
    response.delete_cookie('session_id')
    response.set_cookie(
        'session_id',
        session_id
    )

    return response

