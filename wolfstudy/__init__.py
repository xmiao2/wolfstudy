from config import config
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf.csrf import CsrfProtect

import errno
import os
import sys



bootstrap = Bootstrap()
db = SQLAlchemy()



def install_secret_key(app, filename='secret_key'):
    """Read the secret key from a file in the application's instance
    directory. If the directory or file do not exist, create them and
    write a new secret key from /dev/urandom. We use a file because
    it maintains existing user sessions across server restarts by using
    the same secret key.
    """
    filename = os.path.join(app.instance_path, filename)

    # Make the directory app.instance_path if it does not exist.
    try:
        os.makedirs(app.instance_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(app.instance_path):
            pass
        else:
            raise
    
    # Write 24 random bytes to the file.
    with open(filename, 'a') as f:
        f.write(os.urandom(24))

    # Load the secret key file into app.config.
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print 'Error: Secret key could not be read from %s.' % filename
        sys.exit(1)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    install_secret_key(app)
    CsrfProtect(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
