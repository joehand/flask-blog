from flask.ext.assets import Environment
assets = Environment()

from flask.ext.mail import Mail
mail = Mail()

from flask.ext.misaka import Misaka
md = Misaka()

from flask.ext.mongoengine import MongoEngine
db = MongoEngine()

from flask_s3 import FlaskS3
s3 = FlaskS3()

from flask.ext.security import Security
security = Security()

