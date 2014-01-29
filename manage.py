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
    db.connection.drop_database(app.config['MONGODB_DB'])

    user_datastore = MongoEngineUserDatastore(db, User, Role)

    admin = user_datastore.create_role(name='admin', description='Admin User')
    user = user_datastore.create_user(email='joe.a.hand@gmail.com', password='password')

    user_datastore.add_role_to_user(user, admin)

def shell_context():
    return dict(app=app)

#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()