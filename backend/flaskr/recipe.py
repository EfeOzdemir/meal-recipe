
from flask import (
    Blueprint, request
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from .token import create_token, token_required
import datetime
bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/', methods=["GET"])
def get_recipes():
    db = get_db()
    recipes = db.execute("""
        SELECT recipe.id, title, content, category_id, recipe.cre_date, recipe.user_id, username, category.name as category_name, category_id,
                         (SELECT COUNT(*) FROM likes WHERE recipe_id = recipe.id) as likes
                        FROM recipe 
                        LEFT JOIN user ON recipe.user_id = user.id
                        LEFT JOIN category ON recipe.category_id = category.id 
    """).fetchall()

    print(len(recipes))
    
    return [{"id": row["id"], "title": row["title"], "content": row["content"], 
            "category": {"id": row["category_id"], "name": row["category_name"]}, "likes": row["likes"],
             "user": {"id": row["user_id"], "username": row["username"]},
             "cre_date": row["cre_date"]
             } for row in recipes], 200

@bp.route('/<id>', methods=["GET"])
def get_recipe(id):
    db = get_db()
    recipe = db.execute("""SELECT recipe.id, title, content, category_id, recipe.cre_date, recipe.user_id, username, (SELECT COUNT(*) FROM likes WHERE recipe_id = ?) as likes
                        FROM recipe 
                        LEFT JOIN user ON recipe.user_id = user.id 
                        WHERE recipe.id = ?
    """, (id, id)).fetchone()
    
    if recipe is None:
        return {
            "message": "Recipe not found.",
            "error": "Not found"
        }, 404
    
    comments = db.execute("SELECT comments.id, content, cre_date, user_id, user.username as username FROM comments LEFT JOIN user ON user_id = user.id WHERE recipe_id = ?", (id)).fetchall()
    
    return {"id": recipe["id"], "title": recipe["title"], "content": recipe["content"], 
            "category_id": recipe["category_id"], "likes": recipe["likes"],
             "user": {"id": recipe["user_id"], "username": recipe["username"]},
             "cre_date": recipe["cre_date"], 
             "comments": [
                    {"id": comment["id"], "content": comment["content"], "cre_date": comment["cre_date"], 
                    "user": {
                    "id": comment["user_id"],
                    "username": comment["username"]
                        }
                    } for comment in comments]
            } , 200

@bp.route('/', methods=["POST"])
@token_required
def create_recipe(user):
    recipe_data = request.json

    if not recipe_data:
        return {
            "message": "Provide required fields.",
            "error": "Bad Request"
        }, 400
    
    db = get_db()

    try:
        cursor = db.execute("INSERT INTO recipe (title, content, user_id, category_id, cre_date) VALUES (?, ?, ?, ?, ?)", 
            (recipe_data.get('title'), recipe_data.get('content'), user['id'], recipe_data.get('category_id'), datetime.datetime.now()))
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

@bp.route('/update/<id>', methods=["POST"])
@token_required
def update_recipe(user, id):
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

    if recipe['user_id'] != user['id']:
        return {
            "message": "Permission denied.",
            "error": "Forbidden"
        }, 403

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

@bp.route('/delete/<id>', methods=["DELETE"])
@token_required
def delete_recipe(user, id):
    db = get_db()

    recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id).fetchone()
    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404

    if recipe['user_id'] != user['id']:
        return {
            "message": "Permission denied.",
            "error": "Forbidden"
        }, 403
    
    db.execute("DELETE FROM recipe WHERE id = ?", id)
    db.commit()

    return {"message": "Recipe deleted"}, 200

@bp.route('/comment/<id>', methods = ["POST"])
@token_required
def comment(user, id):
    if not request.json:
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

    content = request.json.get('content')
    try:
        db.execute("INSERT INTO comments (recipe_id, user_id, content, cre_date) VALUES (?, ?, ?, ?)", (id, user['id'], content, datetime.datetime.now()))
        db.commit()
    except db.IntegrityError:
        return {
            "message": "Invalid values.",
            "error": "conflict"
        }, 409

    return {}, 201

@bp.route('/like/<id>', methods = ["POST"])
@token_required
def like(user, id):
    db = get_db()
    recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id)

    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404    
    
    try:
        db.execute("INSERT INTO likes (recipe_id, user_id, cre_date) VALUES (?, ?, ?)", (id, user["id"], datetime.datetime.now()))
        code = 201
    except db.IntegrityError:
        db.execute("DELETE FROM likes WHERE recipe_id = ? AND user_id = ?", (id, user["id"]))
        code = 200
    finally:
        db.commit()

    return {}, code

@bp.route('/save/<id>', methods = ["POST"])
@token_required
def save(user, id):
    db = get_db()
    recipe = db.execute("SELECT * FROM recipe WHERE id = ?", id)

    if recipe is None:
        return {
            "message": "Recipe not found",
            "error": "Not found"
        }, 404    
    
    try:
        db.execute("INSERT INTO saved_recipe (recipe_id, user_id, cre_date) VALUES (?, ?, ?)", (id, user["id"], datetime.datetime.now()))
        code = 201
    except db.IntegrityError:
        db.execute("DELETE FROM saved_recipe WHERE recipe_id = ? AND user_id = ?", (id, user["id"]))
        code = 200
    finally:
        db.commit()

    return {}, code

@bp.route('/category', methods = ["GET"])
def categories():
    db = get_db()
    categories = db.execute("SELECT * FROM category")

    return [{"id": category["id"], "name": category["name"]} for category in categories]