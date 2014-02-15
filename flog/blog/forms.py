from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, RadioField
from wtforms.fields.html5 import DateField, EmailField, URLField
from wtforms.validators import email, length, optional, required, url

from .models import POST_TYPES

class PostForm(Form):
    ''' Form to submit a Post
    '''
    title = TextField('Title', validators=[required()])
    slug = TextField('Slug', validators=[optional()])
    kind = RadioField('Kind', choices=POST_TYPES, default=POST_TYPES[0][0])
    category = TextField('Category', validators=[optional()])
    pub_date = DateField('Publish Date', validators=[optional()])
    link_url = URLField('Link URL', validators=[url(), optional()])


class CommentForm(Form):
    ''' Form to submit a Comment
    '''
    name = TextField('Name*', validators=[required(), length(max=255)])
    email = EmailField('Email', validators=[optional(), email()])
    content = TextAreaField('Leave A Comment*', validators=[required()])