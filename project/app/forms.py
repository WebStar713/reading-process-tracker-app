from django import forms

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        EMPTY_FIELD_ERROR = 'This field is required.'
        model = User
        fields = ('username', 'password')

        error_messages = {'username': {'required': EMPTY_FIELD_ERROR}}
