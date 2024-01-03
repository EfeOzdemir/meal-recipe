
from flask import (
    Blueprint
)

from flaskr.db import get_db
bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users', methods=["GET"])
def get_recipes():
    db = get_db()
    users = db.execute("""
        SELECT * FROM user
    """).fetchall()
    
    return [{"id": row["id"], 
             "username": row['username'],
             "password": row['password'],
             "email": row['email']
             } for row in users], 200
