from flask.ext.wtf import Form
from wtforms import TextField, RadioField
from wtforms.fields.html5 import DateField, URLField
from wtforms.validators import required, optional, url

from .models import POST_TYPES

class PostForm(Form):
    """ Form to submit a Post
    """
    title = TextField('Title', validators=[required()])
    slug = TextField('Slug', validators=[optional()])
    kind = RadioField('Kind', choices=POST_TYPES, default=POST_TYPES[0][0])
    category = TextField('Category', validators=[optional()])
    pub_date = DateField('Published Date', validators=[optional()])
    link_url = URLField('Link URL', validators=[url(), optional()])