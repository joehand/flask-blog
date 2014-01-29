from ..extensions import db
from ..utils import mongo_to_dict
from ..user import User

from datetime import datetime

POST_TYPES = (('static','Static'),
              ('article','Article'), 
              ('link','Link'))

class Post(db.Document):
    user_ref = db.ReferenceField(User)
    slug = db.StringField(unique=True)
    title = db.StringField()
    content = db.StringField()
    kind = db.StringField(choices=POST_TYPES, required=True)
    last_update = db.DateTimeField(default=datetime.now(), required=True)

    meta = {'allow_inheritance': True}

    def to_dict(self):
        return mongo_to_dict(self)

    def clean(self):
        """Clean Data!"""
        if not self.slug:
            self.slug = self.title.replace(' ', '-')

        #Add last update timestamp
        self.last_update = datetime.now()

class Article(Post):
    published = db.BooleanField(default=False, required=True)
    pub_date = db.DateTimeField(required=True)

    def clean(self):
        """Ensures that published essays have a `pub_date` """
        if self.published and self.pub_date is None:
            self.pub_date = datetime.now()

class Link(Post):
    link_url = db.StringField()
