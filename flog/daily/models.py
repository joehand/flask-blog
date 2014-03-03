from datetime import datetime, date
import json
import re

from ..extensions import db
from ..user import User

class Daily(db.Document):
    user_ref = db.ReferenceField(User)
    content = db.StringField()
    date = db.DateTimeField(default=date.today(), required=True, unique_with='user_ref')
    start_time = db.DateTimeField(default=datetime.utcnow(), required=True)
    end_time = db.DateTimeField() # recorded when goal is met
    last_update = db.DateTimeField(default=datetime.utcnow(), required=True)

    meta = {
            'ordering': ['-date']
            }

    def clean(self):
        '''Clean Data!'''
        # Add last update timestamp
        self.last_update = datetime.utcnow()

    def to_dict(self):
        data = json.loads(self.to_json())
        data.pop('_id', None)
        data.pop('_cls', None)
        data['id'] = str(self.id)
        data['user_ref'] = str(self.user_ref.id)
        data['date'] = str(self.date)
        data['start_time'] = str(self.start_time)
        data['end_time'] = str(self.end_time)
        data['last_update'] = str(self.last_update)
        return json.dumps(data)

    def validate_json(self, inputJSON):
        for key, val in inputJSON.items():
            if key in ['content', 'end_time']:
                if key == 'end_time':
                    try:
                        val = datetime.utcfromtimestamp(val/1000.0)
                    except:
                        continue
                    # divide by 1000 because JS timestamp is in ms 
                    # http://stackoverflow.com/questions/10286224/javascript-timestamp-to-python-datetime-conversion
                if val != None and val != 'None': 
                    self[key] = val
            else:
                continue
        self.save()
        return self

    def word_count(self):
        if self.content:
            words = re.findall('\w+', self.content, flags=re.I)
            return len(words)
        return 0

    def goal_met(self):
        goal = Settings.objects(user_ref=self.user_ref).first()
        if self.word_count() > goal.word_goal:
            return True
        return False

class Settings(db.Document):
    user_ref = db.ReferenceField(User)
    word_goal = db.IntField(default=1000)
