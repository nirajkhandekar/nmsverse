from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FieldList
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from flask.ext.wtf.recaptcha import RecaptchaField

class CommentForm(Form):
    name        = StringField('name', validators=[DataRequired()])
    email       = StringField('email', validators=[DataRequired()])
    comment     = StringField('post', widget=TextArea())
    recaptcha   = RecaptchaField()
