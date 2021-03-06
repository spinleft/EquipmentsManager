import pymysql

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="192.168.0.178",
            user="fermi",
            password = "fermi123456",
            database="equipment",
            charset="utf8",
            cursorclass = pymysql.cursors.DictCursor
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
        data = f.read().decode('utf8')
        lines = data.splitlines()
        sql_data = ''
        # 将--注释开头的全部过滤，将空白行过滤
        for line in lines:
            if len(line) == 0:
                continue
            elif line.startswith("--"):
                continue
            else:
                sql_data += line + ' '
        sql_list = sql_data.split(';')[:-1]
        sql_list = [x.replace('\n', ' ') for x in sql_list]
        for sql_item in sql_list:
            cursor.execute(sql_item)
        cursor.close()
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)