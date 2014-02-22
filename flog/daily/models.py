from datetime import datetime, date
import json
import re

from ..extensions import db
from ..user import User

class Daily(db.Document):
    user_ref = db.ReferenceField(User)
    content = db.StringField()
    date = db.DateTimeField(default=date.today(), required=True)

    meta = {
            'ordering': ['-date']
            }

    def to_dict(self):
        data = json.loads(self.to_json())
        data.pop('_id', None)
        data.pop('_cls', None)
        data['id'] = str(self.id)
        data['user_ref'] = str(self.user_ref.id)
        data['date'] = str(self.date)
        return json.dumps(data)

    def validate_json(self, inputJSON):
        for key, val in inputJSON.items():
            if key in ['content']:
                if val != None and val != 'None': 
                    self[key] = val
            else:
                continue
        self.save()
        return self

    def word_count(self):
        words = re.findall('\w+', self.content, flags=re.I)
        return len(words)
