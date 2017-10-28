# config.py

class Config(object):
    """
    Common Configuration
    """
    # for configuration common across all environments


class DevelopmentConfig(Config):
    """
        Development Configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
        Production Configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing Configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
