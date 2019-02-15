import os
base_dir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv(os.path.join(base_dir, '.env'), override=True)


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', default='set_your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default='sqlite:///{}'.format(os.path.join(base_dir, 'db.sqlite')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_METHODS = []


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base_dir, 'data-test.sqlite')
