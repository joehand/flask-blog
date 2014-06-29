# manage.py
import hashlib
import os
import pickle

from flask.ext.assets import ManageAssets
from flask.ext.s3 import create_all
from flask.ext.script import Manager, Shell, Server
from flask.ext.security import MongoEngineUserDatastore
from flask.ext.security.utils import encrypt_password

from jhand import create_app
from jhand.config import ProductionConfig, DevelopmentConfig
from jhand.extensions import db, assets
from jhand.user import User, Role

if os.environ.get('PRODUCTION'):
    app = create_app(config = ProductionConfig)
else:
    app = create_app()

manager = Manager(app)

@manager.command
def initdb():
    '''Init/reset database.'''
    if not os.environ.get('PRODUCTION'):
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
    ''' Builds the js for production
        TODO: Build css here too.
    '''
    jsfile = 'app.min.js'
    os.system('cd jhand/static/js && node libs/r.js -o app.build.js out=../build/%s'%jsfile)
    os.system('cd jhand/static/js && cp libs/require.js ../build/')
    jsfile = 'jhand/static/build/' + jsfile
    md5 = md5sum(jsfile)[:8]
    jsversion = 'app.' + md5 + '.min.js'
    print 'updating js file number to %s' %jsversion
    os.system('cd jhand/static/build/ && cp app.min.js %s'%jsversion)
    pickle_file = 'jhand/static/' + app.config['ASSETS_MANIFEST'].split(':')[1]
    update_pickle(pickle_file, md5)
    os.system('cd jhand/static/build/ && cp app.min.js %s'%jsversion)
    print 'all done with the JS'

def update_pickle(pickle_file, newmd5, blocksize=65536):
    with open(pickle_file, "r+b") as f:
        cache = pickle.load(f)
        for item in cache:
            if 'app' in item and 'js' in item:
                cache[item] = newmd5
    pickle.dump(cache, open(pickle_file, 'wb'))
    return cache

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            hash.update(block)
    return hash.hexdigest()

def clear_css_cache():
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
    print 'starting file upload to Amazon S3'
    create_all(app)
    #TODO : erase old css files on s3
    print 'done with file upload'

@manager.command
def make_production():
    clear_css_cache()
    build_js()
    upload()

def shell_context():
    return dict(app=app)

#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()
