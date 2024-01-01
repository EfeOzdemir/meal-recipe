
from flask import (
    Blueprint, request
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import  cross_origin
from flaskr.db import get_db
from .token import create_token, token_required

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
@cross_origin(origin='*')
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if username is None or password is None or email is None:
        return {
            "message": "Provide user credentials.",
            "data": None,
            "error": "Bad Request"
        }, 400
    
    db = get_db()
    try:
        db.execute(
            "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return {
            "message": "User already exists",
            "data": None,
            "error": "Conflict"
        }, 409
    
    return {
        "message": "Registered succesfully.",
        "data": {"username": username}
    }, 201

@bp.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():

    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        print(username)
        print(password)
        return {
            "message": "Provide user credentials.",
            "data": None,
            "error": "Bad Request"
        }, 400

    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'User not found.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error:
        return {
            "message": error,
            "error": "Unauthorized"
        }, 401

    token = create_token(user)

    return {
        "message": "Login succesfull.",
        "token": token
    }, 200  