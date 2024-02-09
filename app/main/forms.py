from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField



class PostForm(FlaskForm):
    body = PageDownField("Write here", validators=[DataRequired()])
    delete =  SubmitField("Delete")
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = StringField('Enter your answer', validators=[DataRequired()])
    delete =  SubmitField("Delete")
    submit = SubmitField('Submit')

