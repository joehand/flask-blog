from flask.ext.wtf import Form
from wtforms import IntegerField
from wtforms.validators import required

class SettingsForm(Form):
    ''' Form to change settings
    '''
    word_goal = IntegerField('Daily Word Goal')