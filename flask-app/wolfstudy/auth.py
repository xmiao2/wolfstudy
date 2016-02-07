from base64 import b64encode
from pbkdf2 import pbkdf2_hex
import hashlib
import os

from wolfstudy import app
import db

def register_user(email, username, password):
    """Register a user with the given email, username, and password. Uses PBKDF2 on the password
    to generate and store a salt and hash with many iterations before adding the user to the database.
    The password must be encoded in UTF-8 instead of Unicode so that PBKDF2 can run correctly.
    """

    # Get a random seed from /dev/urandom for the salt
    salt_bytes = os.urandom(24)
    salt = b64encode(salt_bytes).decode('utf-8')

    iterations = app.config['HASH_ITERATIONS']
    keylen     = app.config['KEY_LENGTH']

    # Run PBKDF2 with password and seed
    pass_hash = pbkdf2_hex(password, salt, iterations=iterations, keylen=keylen, hashfunc=hashlib.sha256)

    # Store the username, iterations, seed, and hashed password in the database
    db.db_add_user(username, email, iterations, salt, pass_hash)
