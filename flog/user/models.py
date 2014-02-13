from flask.ext.security import login_required, RoleMixin, UserMixin

from ..extensions import db
from ..utils import mongo_to_dict


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.DynamicDocument, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    current_login_ip = db.StringField()
    login_count = db.IntField()

    def to_dict(self):
        return mongo_to_dict(self)

    def get(self, key, no_attr=None):
        try:
            return self[key]
        except KeyError:
            return no_attr
