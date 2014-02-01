from ..extensions import db
from ..utils import mongo_to_dict
from ..user import User

from datetime import datetime
import json


ILLEGAL_SLUGS = ['admin', 'notes', 'archives']

POST_TYPES = (('article','Article'),
              ('note','Note'), 
              ('page','Page'))

class Post(db.Document):
    user_ref = db.ReferenceField(User)
    slug = db.StringField(unique=True)
    title = db.StringField()
    content = db.StringField()
    kind = db.StringField(choices=POST_TYPES, required=True)
    last_update = db.DateTimeField(default=datetime.now(), required=True)
    published = db.BooleanField(default=False, required=True)
    pub_date = db.DateTimeField()

    meta = {
            'allow_inheritance': True, 
            'ordering': ['-last_update','-pub_date']
            }

    def to_dict(self):
        data = json.loads(self.to_json())
        data.pop("_id", None)
        data.pop("_cls", None)
        data['id'] = str(self.id)
        data['user_ref'] = str(self.user_ref.id)
        data['last_update'] = str(self.last_update)
        data['pub_date'] = str(self.pub_date)
        return json.dumps(data)

    def clean(self):
        """Clean Data!"""
        if not self.slug:
            self.slug = self.title.replace(' ', '-').lower()

        if self.slug in ILLEGAL_SLUGS:
            self.slug = self.slug + '1' #todo: make this more robust

        # Ensures that published essays have a `pub_date`
        if self.published and self.pub_date is None:
            self.pub_date = datetime.now()

        #Add last update timestamp
        self.last_update = datetime.now()

class Article(Post):
    category = db.StringField()
    subtitle = db.StringField()

class Note(Post):
    link_url = db.StringField()
