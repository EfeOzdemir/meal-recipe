
from flask import (
    Blueprint, request
)
import pymysql
from flaskr.db import get_db
from .token import token_required, token_check
import datetime
import base64

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/', methods=["GET"])
def get_recipes():
    db = get_db()
    cursor = db.cursor()
    args = request.args

    if(args.get('c') is None):
        cursor.execute("""
            SELECT recipe.id, title, content, image, category_id, recipe.cre_date, recipe.user_id, username, category.name as category_name, category_id,
                (SELECT COUNT(*) FROM likes WHERE recipe_id = recipe.id) as likes
                FROM recipe 
                LEFT JOIN user ON recipe.user_id = user.id
                LEFT JOIN category ON recipe.category_id = category.id
        """)
    else:
        cursor.execute("""
            SELECT recipe.id, title, content, image, category_id, recipe.cre_date, recipe.user_id, username, category.name as category_name, category_id,
                (SELECT COUNT(*) FROM likes WHERE recipe_id = recipe.id) as likes
                FROM recipe 
                LEFT JOIN user ON recipe.user_id = user.id
                LEFT JOIN category ON recipe.category_id = category.id 
                WHERE category_id = %s
        """, (args.get('c'),))

    recipes = cursor.fetchall()

    return [{"id": row["id"], "title": row["title"], "content": row["content"], "image": 'data:image/jpeg;base64,' + row["image"],
            "category": {"id": row["category_id"], "name": row["category_name"]}, "likes": row["likes"],
             "user": {"id": row["user_id"], "username": row["username"]},
             "cre_date": row["cre_date"]
             } for row in recipes], 200

@bp.route('/<id>', methods=["GET"])
@token_check
def get_recipe(user, id):
    db = get_db()
    cursor = db.cursor()
    if 'id' in user:
        cursor.execute("""SELECT recipe.id, title, content, image, category_id, recipe.cre_date, recipe.user_id, username, 
                        (SELECT COUNT(*) FROM likes WHERE recipe_id = %s) as likes,
                        (SELECT EXISTS(recipe_id) FROM likes WHERE recipe_id = %s and user_id = %s) as isLiked
                        FROM recipe 
                        LEFT JOIN user ON recipe.user_id = user.id
                        WHERE recipe.id = %s
                    """, (id, id, user['id'], id))
    else:
        cursor.execute("""SELECT recipe.id, title, content, image, category_id, recipe.cre_date, recipe.user_id, username, 
                        (SELECT COUNT(*) FROM likes WHERE recipe_id = %s) as likes
                        FROM recipe 
                        LEFT JOIN user ON recipe.user_id = user.id
                        WHERE recipe.id = %s
                    """, (id, id))
    recipe = cursor.fetchone()

    if 'isLiked' not in recipe:
        recipe['isLiked'] = False
    
    if recipe is None:
        return {"message": "Recipe not found.", "error": "Not found"}, 404
    
    cursor.execute("SELECT comments.id, content, cre_date, user_id, user.username as username FROM comments LEFT JOIN user ON user_id = user.id WHERE recipe_id = %s", (id,))
    comments = cursor.fetchall()
    
    return {"id": recipe["id"], "title": recipe["title"], "content": recipe["content"], "image": 'data:image/jpeg;base64,' + recipe["image"], 
            "category_id": recipe["category_id"], "likes": recipe["likes"],
             "user": {"id": recipe["user_id"], "username": recipe["username"]},
             "isLiked": recipe['isLiked'],
             "cre_date": recipe["cre_date"], 
             "ingredients": recipe["ingredients"],
             "comments": [{"id": comment["id"], "content": comment["content"], "cre_date": comment["cre_date"], 
                           "user": {"id": comment["user_id"], "username": comment["username"]}} for comment in comments]
            }, 200

@bp.route('/', methods=["POST"])
@token_required
def create_recipe(user):
    recipe_data = request.form
    print(recipe_data)
    if not recipe_data:
        return {"message": "Provide required fields.", "error": "Bad Request"}, 400

    print(request.files)
    conn = get_db()
    db = conn.cursor()

    try:
        image_file = request.files['image']
        image_data = image_file.read()
        image_string = base64.b64encode(image_data)
        db.execute("INSERT INTO recipe (title, content, image, ingredients, user_id, category_id, cre_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (recipe_data.get('title'), recipe_data.get('content'), image_string, user['id'], recipe_data.get('category_id'), datetime.datetime.now()))
        conn.commit()
    except pymysql.IntegrityError:
        conn.rollback()
        return {"message": "Invalid values.", "error": "Conflict"}, 409

    return {"message": "Recipe created successfully."}, 201

@bp.route('/update/<id>', methods=["POST"])
@token_required
def update_recipe(user, id):
    recipe_data = request.json
    if not recipe_data:
        return {"message": "Provide required fields.", "error": "Bad Request"}, 400
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM recipe WHERE id = %s", (id,))
    recipe = cursor.fetchone()
    if recipe is None:
        return {"message": "Recipe not found", "error": "Not found"}, 404

    if recipe['user_id'] != user['id']:
        return {"message": "Permission denied.", "error": "Forbidden"}, 403

    cursor.execute("UPDATE recipe SET title = %s, content = %s, category_id = %s WHERE id = %s", 
                   (recipe_data.get('title'), recipe_data.get('content'), recipe_data.get('category_id'), id))
    db.commit()
    
    return {}, 204

@bp.route('/delete/<id>', methods=["DELETE"])
@token_required
def delete_recipe(user, id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM recipe WHERE id = %s", (id,))
    recipe = cursor.fetchone()
    if recipe is None:
        return {"message": "Recipe not found", "error": "Not found"}, 404

    if recipe['user_id'] != user['id']:
        return {"message": "Permission denied.", "error": "Forbidden"}, 403

    cursor.execute("DELETE FROM recipe WHERE id = %s", (id,))
    db.commit()

    return {"message": "Recipe deleted"}, 200

@bp.route('/comment/<id>', methods=["POST"])
@token_required
def comment(user, id):
    comment_data = request.json
    if not comment_data or 'content' not in comment_data:
        return {"message": "Provide required fields.", "error": "Bad Request"}, 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM recipe WHERE id = %s", (id,))
    if cursor.fetchone() is None:
        return {"message": "Recipe not found", "error": "Not found"}, 404

    cursor.execute("INSERT INTO comments (recipe_id, user_id, content, cre_date) VALUES (%s, %s, %s, %s)", 
                   (id, user['id'], comment_data['content'], datetime.datetime.now()))
    db.commit()

    return {"message": "Comment added successfully"}, 201

@bp.route('/like/<id>', methods=["POST"])
@token_required
def like(user, id):
    db = get_db()
    cursor = db.cursor()

    if not user:
        return {"message": "Sing in required"}, 403

    cursor.execute("SELECT * FROM likes WHERE recipe_id = %s AND user_id = %s", (id, user["id"]))
    if cursor.fetchone():
        cursor.execute("DELETE FROM likes WHERE recipe_id = %s AND user_id = %s", (id, user["id"]))
        message = "Like removed"
    else:
        cursor.execute("INSERT INTO likes (recipe_id, user_id, cre_date) VALUES (%s, %s, %s)", (id, user["id"], datetime.datetime.now()))
        message = "Recipe liked"
    db.commit()

    return {"message": message}, 200

@bp.route('/save/<id>', methods=["POST"])
@token_required
def save(user, id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM saved_recipe WHERE recipe_id = %s AND user_id = %s", (id, user["id"]))
    if cursor.fetchone():
        # If already saved, remove from saved recipes
        cursor.execute("DELETE FROM saved_recipe WHERE recipe_id = %s AND user_id = %s", (id, user["id"]))
        message = "Recipe removed from saved recipes"
    else:
        # If not saved, add to saved recipes
        cursor.execute("INSERT INTO saved_recipe (recipe_id, user_id, cre_date) VALUES (%s, %s, %s)", 
                       (id, user["id"], datetime.datetime.now()))
        message = "Recipe saved successfully"

    db.commit()
    return {"message": message}, 200

@bp.route('/category', methods=["GET"])
def categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    return [{"id": category["id"], "name": category["name"]} for category in categories], 200