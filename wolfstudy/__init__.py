from contextlib import closing
from flask import Flask, g
from wolfstudy import config

import os.path
import sqlite3
import sys



# Create and configure Flask object
app = Flask(__name__)
app.config.from_object(config)

def get_secret_key(filename='secret_key'):
    """Get the SECRET_KEY from a file in the instance directory.

    If the file does not exist, print instructions to create it from
    a shell with a random key, then exit.
    """

    filename = os.path.join(app.instance_path, filename)
    try:
        return open(filename, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        if not os.path.isdir(os.path.dirname(filename)):
            print 'mkdir -p', os.path.dirname(filename)
        print 'head -c 24 /dev/urandom >', filename
        sys.exit(1)

app.config['SECRET_KEY'] = get_secret_key()



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
    # Open a connection to the database and store the cursor in g.
    g.db = connect_db()
    g.cursor = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    # Close the database connection.
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



import wolfstudy.views
