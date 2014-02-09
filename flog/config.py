import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    PROJECT = "flog"

    # Get app root path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True

    SECRET_KEY = 'this_is_so_secret' #used for development, reset in prod

    # Flask Security Config
    SECURITY_TRACKABLE = True

    DEBUG_TB_ENABLED = False

    S3_BUCKET_NAME = 'joehand_blog'

    S3_HEADERS = {
        'Expires': 'Thu, 15 Feb 2014 20:00:00 GMT',
        'Cache-Control': 'max-age=86400',
    }

    SECURITY_PASSWORD_HASH = 'bcrypt'

class ProductionConfig(Config):

    PRODUCTION = True

    SECRET_KEY = 'test'

    SECURITY_PASSWORD_SALT = 'test'

    DEBUG = True

    ASSETS_AUTO_BUILD = False

    USE_S3_DEBUG = True

    #MongoDB Info
    MONGODB_DB = os.environ.get('MONGODB_DATABASE')
    MONGODB_HOST= os.environ.get('MONGODB_HOST')
    MONGODB_PORT= os.environ.get('MONGODB_PORT')
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')

class DevelopmentConfig(Config): 

    # MongoDB Config
    MONGODB_DB = 'blog_db'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SECURITY_PASSWORD_SALT = '/2aX16zPnnIgfMwkOjGX4S'

    DEBUG_TB_PANELS = (
        'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel',
        'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
        'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
        'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel'
    )

class TestingConfig(Config):
    
    TESTING = True