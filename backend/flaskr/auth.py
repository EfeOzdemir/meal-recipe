
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
        return {"message": "Provide user credentials.", "data": None, "error": "Bad Request"}, 400
    
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
            (username, email, generate_password_hash(password))
        )
        db.commit()
    except pymysql.IntegrityError:
        db.rollback()  # Roll back the transaction on error
        return {"message": "User already exists", "data": None, "error": "Conflict"}, 409
    
    return {"message": "Registered succesfully.", "data": {"username": username}}, 201

@bp.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return {"message": "Provide user credentials.", "data": None, "error": "Bad Request"}, 400

    db = get_db()
    cursor = db.cursor()
    error = None
    cursor.execute(
        'SELECT * FROM user WHERE username = %s', (username,)
    )
    user = cursor.fetchone()

    if user is None:
        error = 'User not found.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error:
        return {"message": error, "error": "Unauthorized"}, 401

    token = create_token(user)

    return {"message": "Login successful.", "token": token}, 200