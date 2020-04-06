
# Default config
class BaseConfig(object):
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig(BaseConfig):
    DEBUG = True
    Testing = True
    WTF_CSRF_ENABLED = False
