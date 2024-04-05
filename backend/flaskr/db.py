import pymysql
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="database.cbkiea6yaw92.eu-central-1.rds.amazonaws.com",
            user="admin",
            password="password",
            db="application",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        # MySQL might not allow multiple commands by default, so split them.
        sql_commands = f.read().decode('utf8').split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)

    # It's important to commit changes
    db.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)