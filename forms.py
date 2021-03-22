from wtforms import SelectField, HiddenField
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelForm

from models import PostObj, UsersObj


class PostForm(ModelForm):
    category = SelectField('category', [InputRequired()], coerce=int)
    author = HiddenField()

    class Meta:
        model = PostObj
        exclude = ('available', 'created')


class LoginForm(ModelForm):

    class Meta:
        model = UsersObj
        only = ('login', 'passwd')
