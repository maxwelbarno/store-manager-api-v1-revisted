import os


class Config(object):
    """ Parent configuration class """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED')
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = False

# Testing configrations


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database"""
    TESTING = True
    DEBUG = True

# staging setting


class StagingConfig(Config):
    """Configurations for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Productions"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
