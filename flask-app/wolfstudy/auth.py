from base64 import b64encode
from pbkdf2 import pbkdf2_hex
import hashlib
import os

from wolfstudy import app
import db

def get_pass_hash(password, salt, iterations, key_length):
    password = password.encode('utf-8')

    # Run PBKDF2 with password and seed
    return pbkdf2_hex(password, salt, iterations=iterations, keylen=key_length, hashfunc=hashlib.sha256)

def register_user(email, username, password):
    """Register a user with the given email, username, and password. Uses PBKDF2 on the password
    to generate and store a salt and hash with many iterations before adding the user to the database.
    The password must be encoded in UTF-8 instead of Unicode so that PBKDF2 can run correctly.
    """

    # Get a random seed from /dev/urandom for the salt
    salt_bytes = os.urandom(24)
    salt = b64encode(salt_bytes).decode('utf-8')

    iterations = app.config['HASH_ITERATIONS']
    key_length = app.config['KEY_LENGTH']

    pass_hash = get_pass_hash(password, salt, iterations, key_length)

    # Store the username, iterations, seed, and hashed password in the database
    db.db_add_user(username, email, iterations, salt, pass_hash)

def is_valid_login(username, password):
    """Determine if the given username and password is a valid login. Check that the username and password
    are in the database and that the password correctly authenticates the username. Return True if this is
    a valid login, return False if it is an invalid login.
    """

    # Check if the username is in the database.
    if not db.db_username_exists(username):
        return False
    
    salt = db.db_get_salt(username)
    iterations = app.config['HASH_ITERATIONS']
    key_length = app.config['KEY_LENGTH']

    pass_hash_attempt = get_pass_hash(password, salt, iterations, key_length)
    pass_hash_actual  = db.db_get_pass_hash(username)

    return pass_hash_attempt == pass_hash_actual
