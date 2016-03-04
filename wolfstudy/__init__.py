from contextlib import closing
from flask import Flask, g, current_app
from config import config

from main import main

import sqlite3
import os
import sys



def install_secret_key(app, filename='secret_key'):
    filename = os.path.join(app.instance_path, filename)
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        if not os.path.isdir(os.path.dirname(filename)):
            print 'mkdir -p', os.path.dirname(filename)
        print 'head -c 24 /dev/urandom >', filename
        sys.exit(1)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    install_secret_key(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



def connect_db():
    """Connect to the database specified in app.config."""
    return sqlite3.connect(current_app.config['DATABASE'])

def init_db():
    """Create and set up the database specified in app.config."""
    with closing(connect_db()) as db:
        with current_app.open_resource('schema.sql', mode='r') as f:
            schema_script = f.read()
            db.cursor().executescript(schema_script)
        db.commit()



@main.before_request
def before_request():
    # Open a connection to the database and store the cursor in g.
    g.db = connect_db()
    g.cursor = g.db.cursor()

@main.teardown_request
def teardown_request(exception):
    # Close the database connection.
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
