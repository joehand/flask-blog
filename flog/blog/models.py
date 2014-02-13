from ..extensions import db
from ..utils import mongo_to_dict, slugify
from ..user import User
from .constants import *

from datetime import datetime
from urlparse import urlparse
import json

class Post(db.Document):
    user_ref = db.ReferenceField(User)
    slug = db.StringField(unique=True)
    title = db.StringField()
    content = db.StringField()
    kind = db.StringField(choices=POST_TYPES, required=True)
    last_update = db.DateTimeField(default=datetime.now(), required=True)
    published = db.BooleanField(default=False, required=True)
    pub_date = db.DateTimeField()
    category = db.StringField()
    link_url = db.StringField()

    meta = {
            'allow_inheritance': True, 
            'ordering': ['-pub_date','-last_update']
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
            self.slug = slugify(self.title)

        if self.slug in ILLEGAL_SLUGS:
            self.slug = self.slug + '1' #todo: make this more robust

        # Add last update timestamp
        self.last_update = datetime.now()

        if self.pub_date is None:
        # Ensures that everything has a `pub_date`
            self.pub_date = datetime.now().strftime('%Y-%m-%d')

        if self.kind == 'note':
            self.category = 'note'
        elif self.kind == 'article' and self.category is None:
            self.category = 'uncategorized'

    def validate_json(self, inputJSON):
        for key, val in inputJSON.items():
            if key not in ACCEPTED_KEYS:
                continue
            if key == 'content':
                val = val #may need to clean or do markdown processing
            if key == 'category':
                val = val.strip().lower()
            if key == 'title':
                val = val.strip()
            if key == 'slug':
                val = val.strip().replace(' ', '-')
            if key == 'link_url':
                val = urlparse(val).geturl()
            if key == 'pub_date' and val != 'None':
                val = datetime.strptime(val.split(' ')[0], '%Y-%m-%d')
            if key == 'published':
                if isinstance(val, basestring):
                    if val.lower() == 'false':
                        val = False
                    elif val.lower() == 'true':
                        val = True
            if val != None and val != 'None': 
                self[key] = val

        self.save()
        return self
