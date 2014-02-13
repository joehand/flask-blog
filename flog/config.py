import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    PROJECT = 'flog'

    # Get app root path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True

    SECRET_KEY = 'this_is_so_secret' #used for development, reset in prod

    # Flask Security Config
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True

    DEBUG_TB_ENABLED = False

    S3_BUCKET_NAME = 'joehand_blog'

    S3_HEADERS = {
        'Expires': 'Thu, 15 Feb 2014',
        'Cache-Control': 'max-age=86400',
    }

    SECURITY_PASSWORD_HASH = 'bcrypt'

    S3_UPLOAD_DIRECTORY = 'backup'

class ProductionConfig(Config):

    PRODUCTION = True

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

    DEBUG = False

    ASSETS_AUTO_BUILD = False

    #MongoDB Info
    MONGODB_DB = os.environ.get('MONGODB_DATABASE')
    MONGODB_HOST = os.environ.get('MONGO_URL')
    MONGODB_PORT = os.environ.get('MONGODB_PORT')
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

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