import os


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DB_URI = 'sqlite:///data.db'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_URI = 'sqlite:///dev.db'
    SECRET_KEY = 'DEV_KEY'


class TestConfig(Config):
    """Test configuration."""
    ENV = 'test'
    TESTING = True
    DEBUG = True
    DB_URI = 'sqlite:///'
    SECRET_KEY = 'TEST_KEY'
    LOGIN_DISABLED = True
