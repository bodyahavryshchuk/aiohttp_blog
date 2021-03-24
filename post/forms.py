from wtforms import SelectField, HiddenField
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelForm

from .models import PostObj, CommentObj


class PostForm(ModelForm):
    category = SelectField('category', [InputRequired()], coerce=int)
    author = HiddenField()

    class Meta:
        model = PostObj
        exclude = ('available', 'created')


class CommentForm(ModelForm):
    post = HiddenField()
    author = HiddenField()

    class Meta:
        model = CommentObj
        exclude = ('available', 'created')
