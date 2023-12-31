
from flask import (
    Blueprint, request
)
from werkzeug.security import generate_password_hash
from flaskr.db import get_db
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users', methods=["GET"])
def get_users():
    db = get_db()
    users = db.execute("""
        SELECT * FROM user
    """).fetchall()
    
    return [{"id": row["id"], 
             "username": row['username'],
             "password": row['password'],
             "email": row['email']
             } for row in users], 200


@bp.route('/user/<id>', methods=["GET"])
def get_user(id):
    db = get_db()
    user = db.execute("""
        SELECT * FROM user WHERE id = ?
    """, (id)).fetchone()
    
    return {"id": user["id"], 
             "username": user['username'],
             "email": user['email']
             }

@bp.route('/user/edit/<id>', methods=["POST"])
def edit_user(id):
    db = get_db()
    user = db.execute("""
        SELECT * FROM user WHERE id = ?
    """, (id)).fetchone()

    if user is None:
        return {
            "message": "User not found",
            "error": "Not found"
        }, 404
    
    user_data = request.json

    try:
        if user_data.get('password'):
            db.execute("UPDATE user SET username = ?, password = ?, email = ? WHERE id = ?", 
                    (user_data.get('username'), generate_password_hash(user_data.get('password')), user_data.get('email'), id))
        else:
            db.execute("UPDATE user SET username = ?, email = ? WHERE id = ?", 
                (user_data.get('username'), user_data.get('email'), id))
        db.commit()
    except db.IntegrityError:
        return {
            "message": "Invalid values.",
            "error": "Conflict"
        }, 409
        
    return {}, 204


@bp.route('/user/delete/<id>', methods=["DELETE"])
def delete_user(id):
    db = get_db()
    user = db.execute("""
        SELECT * FROM user WHERE id = ?
    """, (id)).fetchone()

    if user is None:
        return {
            "message": "User not found",
            "error": "Not found"
        }, 404
    
    db.execute("DELETE FROM user WHERE id = ?",(id))
    db.commit()

    return {}, 204            

@bp.route('recipe/delete/<id>', methods=["DELETE"])
def delete_recipe(id):
    db = get_db()

    recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id).fetchone()
    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404
    
    db.execute("DELETE FROM recipe WHERE id = ?", id)
    db.commit()

    return {"message": "Recipe deleted"}, 200


@bp.route('/recipe/create', methods=["POST"])
def create_recipe():
    recipe_data = request.json

    if not recipe_data:
        return {
            "message": "Provide required fields.",
            "error": "Bad Request"
        }, 400
    
    db = get_db()

    try:
        cursor = db.execute("INSERT INTO recipe (title, content, user_id, category_id, cre_date) VALUES (?, ?, ?, ?, ?)", 
            (recipe_data.get('title'), recipe_data.get('content'), 3, recipe_data.get('category_id'), datetime.datetime.now()))
        db.commit()
        
        id = cursor.lastrowid
        db.executemany("INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?)", [(id, ingredient) for ingredient in recipe_data.get('ingredients')])

        db.commit()
    except db.IntegrityError:
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
    
    db = get_db()

    recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id).fetchone()
    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404

    try:
        db.execute("UPDATE recipe SET title = ?, content = ?, category_id = ? WHERE id = ?", 
                   (recipe_data.get('title'), recipe_data.get('content'), recipe_data.get('category_id'), id))
        db.commit()
    except db.IntegrityError:
        return {
            "message": "Invalid values.",
            "error": "Conflict"
        }, 409
    
    return {}, 204

@bp.route('/infos', methods = ["GET"])
def get_infos():
    db = get_db()
    infos = db.execute("SELECT category.name as category_name, count(*) as count FROM recipe LEFT JOIN category ON category_id = category.id GROUP BY category_id").fetchall()

    return [{"category_name": info["category_name"], "count": info["count"]} for info in infos], 200

@bp.route('/infos/comment', methods = ["GET"])
def get_recipe_comment_infos():
    db = get_db()
    infos = db.execute("SELECT recipe.title as recipe_title, count(*) as count FROM comments LEFT JOIN recipe ON recipe_id = recipe.id GROUP BY recipe_id").fetchall()

    return [{"recipe_name": info["recipe_title"], "count": info["count"]} for info in infos], 200