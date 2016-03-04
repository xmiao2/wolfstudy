import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    KEY_LENGTH      = 32    # The length of password hashes. Do not change this - passwords won't authenticate with different hash lengths.
    HASH_ITERATIONS = 16384 # = 2^16. Number of hash iterations to perform when hashing a user's password.

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = os.path.join(basedir, 'wolfstudy-dev.sqlite')

class ProductionConfig(Config):
    DATABASE = os.path.join(basedir, 'wolfstudy.sqlite')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}
