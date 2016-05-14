from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FieldList
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class PostForm(Form):
    title       = StringField('title', validators=[DataRequired()])
    description = StringField('description', widget=TextArea())
    tags        = StringField('tags')
    post        = StringField('post', widget=TextArea())
    author      = StringField('author')
