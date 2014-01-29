from ..extensions import db
from ..utils import mongo_to_dict

from flask.ext.security import UserMixin, RoleMixin, login_required


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.DynamicDocument, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def to_dict(self):
        return mongo_to_dict(self)

    def get(self, key, no_attr=None):
        try:
            return self[key]
        except KeyError:
            return no_attr
