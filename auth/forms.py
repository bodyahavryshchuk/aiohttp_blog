from wtforms_alchemy import ModelForm

from .models import UsersObj


class LoginForm(ModelForm):

    class Meta:
        model = UsersObj
        only = ('login', 'passwd')
