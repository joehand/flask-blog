from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import required, optional

from .models import POST_TYPES

class PostForm(Form):
    """ Form to submit a Post
    """
    title = TextField('Title', description='',
                       validators=[required()])
    slug = TextField('Slug', description='',
                       validators=[optional()])
    kind = SelectField('Kind', choices=POST_TYPES)