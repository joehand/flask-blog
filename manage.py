# manage.py
from flask.ext.script import Manager, Shell, Server
from flask.ext.security import MongoEngineUserDatastore

from flog import create_app
from flog.extensions import db
from flog.user import User, Role

app = create_app()
manager = Manager(app)

@manager.command
def initdb():
    """Init/reset database."""
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    user_datastore.create_user(email='joe.a.hand@gmail.com', password='password')

def shell_context():
    return dict(app=app)

#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()