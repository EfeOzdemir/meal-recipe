from flask import (
    Blueprint, request
)
from werkzeug.security import generate_password_hash
from flaskr.db import get_db
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')
import pymysql

@bp.route('/users', methods=["GET"])
def get_users():
    conn = get_db()
    db = conn.cursor(pymysql.cursors.DictCursor)
    db.execute("""
        SELECT * FROM user
    """)
    users = db.fetchall()

    return [{"id": row["id"], 
             "username": row['username'],
             "password": row['password'],
             "email": row['email']
             } for row in users], 200

@bp.route('/user/<id>', methods=["GET"])
def get_user(id):
    conn = get_db()
    db = conn.cursor(pymysql.cursors.DictCursor)
    db.execute("""
        SELECT * FROM user WHERE id = %s
    """, (id,))
    user = db.fetchone()

    if user:
        return {"id": user["id"], 
                "username": user['username'],
                "email": user['email']
                }
    else:
        return {"message": "User not found", "error": "Not found"}, 404
    
@bp.route('/user/edit/<id>', methods=["POST"])
def edit_user(id):
    conn = get_db()
    db = conn.cursor()
    db.execute("""
        SELECT * FROM user WHERE id = %s
    """, (id,))
    user = db.fetchone()

    if user is None:
        return {"message": "User not found", "error": "Not found"}, 404

    user_data = request.json

    try:
        if user_data.get('password'):
            db.execute("UPDATE user SET username = %s, password = %s, email = %s WHERE id = %s", 
                       (user_data.get('username'), generate_password_hash(user_data.get('password')), user_data.get('email'), id))
        else:
            db.execute("UPDATE user SET username = %s, email = %s WHERE id = %s", 
                       (user_data.get('username'), user_data.get('email'), id))
        conn.commit()
    except pymysql.IntegrityError:
        conn.rollback()
        return {"message": "Invalid values.", "error": "Conflict"}, 409

    return {}, 204


@bp.route('/user/delete/<id>', methods=["DELETE"])
def delete_user(id):
    conn = get_db()
    db = conn.cursor()
    db.execute("DELETE FROM user WHERE id = %s",(id,))
    conn.commit()
    return {}, 204       

@bp.route('/recipe/delete/<id>', methods=["DELETE"])
def delete_recipe(id):
    conn = get_db()
    db = conn.cursor()

    recipe = db.execute("SELECT * FROM recipe WHERE id = %s", (id,)).fetchone()
    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404
    
    db.execute("DELETE FROM recipe WHERE id = %s", (id,))
    conn.commit()

    return {"message": "Recipe deleted"}, 200


@bp.route('/recipe/create', methods=["POST"])
def create_recipe():
    recipe_data = request.json

    if not recipe_data:
        return {
            "message": "Provide required fields.",
            "error": "Bad Request"
        }, 400
    
    conn = get_db()
    db = conn.cursor()

    try:
        db.execute("INSERT INTO recipe (title, content, user_id, category_id, cre_date) VALUES (%s, %s, %s, %s, %s)", 
            (recipe_data.get('title'), recipe_data.get('content'), 3, recipe_data.get('category_id'), datetime.datetime.now()))
        conn.commit()
        
        id = db.lastrowid
        db.executemany("INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (%s, %s)", [(id, ingredient) for ingredient in recipe_data.get('ingredients')])

        conn.commit()
    except pymysql.IntegrityError:
        return {
            "message": "Invalid values.",
            "error": "Conflict"
        }, 409
    
    return {
        "message": "Recipe created succesfully.",
    }, 201

@bp.route('/recipe/edit/<id>', methods=["POST"])
def update_recipe(id):
    recipe_data = request.json
    if not recipe_data:
        return {
            "message": "Provide required fields.",
            "error": "Bad Request"
        }, 400
    
    conn = get_db()
    db = conn.cursor()

    recipe = db.execute("SELECT * FROM recipe WHERE id = %s", (id,)).fetchone()
    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404

    try:
        db.execute("UPDATE recipe SET title = %s, content = %s, category_id = %s WHERE id = %s", 
                   (recipe_data.get('title'), recipe_data.get('content'), recipe_data.get('category_id'), id))
        conn.commit()
    except pymysql.IntegrityError:
        return {
            "message": "Invalid values.",
            "error": "Conflict"
        }, 409
    
    return {}, 204

@bp.route('/infos', methods = ["GET"])
def get_infos():
    conn = get_db()
    db = conn.cursor(pymysql.cursors.DictCursor)
    db.execute("SELECT category.name as category_name, count(*) as count FROM recipe LEFT JOIN category ON category_id = category.id GROUP BY category_id")
    infos = db.fetchall()

    return [{"category_name": info["category_name"], "count": info["count"]} for info in infos], 200

@bp.route('/infos/comment', methods = ["GET"])
def get_recipe_comment_infos():
    conn = get_db()
    db = conn.cursor(pymysql.cursors.DictCursor)
    db.execute("SELECT recipe.title as recipe_title, count(*) as count FROM comments LEFT JOIN recipe ON recipe_id = recipe.id GROUP BY recipe_id")
    infos = db.fetchall()

    return [{"recipe_name": info["recipe_title"], "count": info["count"]} for info in infos], 200
