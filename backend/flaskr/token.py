import jwt
import functools
from .db import get_db
from flask import current_app, request

def create_token(user):
    token = jwt.encode(
        {
            "id": user["id"],
            "username": user['username']
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            print(request.headers)
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        decoded_token = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        db = get_db()

        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (decoded_token['id'],)
        ).fetchone()

        if user is None:
            return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        return f(user, *args, **kwargs)

    return decorated
