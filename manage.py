# manage.py
from flask.ext.script import Manager, Shell, Server
from flask.ext.security import MongoEngineUserDatastore
from flask.ext.security.utils import encrypt_password
from flask.ext.s3 import create_all
from flask.ext.assets import ManageAssets

from flog import create_app
from flog.extensions import db, assets
from flog.user import User, Role

import os
import bcrypt

app = create_app()
manager = Manager(app)

@manager.command
def initdb():
    """Init/reset database."""
    db.connection.drop_database(app.config['MONGODB_DB'])

    user_datastore = MongoEngineUserDatastore(db, User, Role)

            
    admin = user_datastore.create_role(name='admin', description='Admin User')
    user = user_datastore.create_user(
        email='joe.a.hand@gmail.com', 
        password=encrypt_password('password')
    )

    user_datastore.add_role_to_user(user, admin)

@manager.command
def build_js():
    """ Builds the js for production
        TODO: Build css here too. 
    """
    jsfile = 'app.min.js'
    os.system('cd flog/static/js && node libs/r.js -o app.build.js out=../build/%s'%jsfile)
    os.system('cd flog/static/js && cp libs/require.js ../build/')
    jsfile = 'flog/static/build/' + jsfile

@manager.command
def build_css():
    import logging
    from webassets.script import CommandLineEnvironment

    # Setup a logger
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)

    cmdenv = CommandLineEnvironment(assets, log)
    cmdenv.clean()


@manager.command
def upload():
    create_all(app)

def shell_context():
    return dict(app=app)

#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()