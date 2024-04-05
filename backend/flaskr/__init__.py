import os
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, support_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MYSQL_USER="meal-recipe",
        MYSQL_PASSWORD="mealRecipe",
        MYSQL_DB="meal-recipe",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth, recipe, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(recipe.bp)
    app.register_blueprint(admin.bp)

    return app