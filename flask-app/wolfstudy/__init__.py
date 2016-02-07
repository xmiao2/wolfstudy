from contextlib import closing
from flask import Flask, g
from wolfstudy import config

import sqlite3

# Create and configure Flask object
app = Flask(__name__)
app.config.from_object(config)

def connect_db():
    """Connect to the database specified in app.config."""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """Create and set up the database specified in app.config."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            schema_script = f.read()
            db.cursor().executescript(schema_script)
        db.commit()

@app.before_request
def before_request():
    # Open a connection to the database and store it in g.
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    # Close the database connection.
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

import wolfstudy.views
