from django import forms

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form_control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form_control"}))

    username.widget.attrs['size'] = '100'


    class Meta:
        EMPTY_FIELD_ERROR = 'This field is required.'
        model = User
        fields = ('username', 'password')

        error_messages = {'username': {'required': EMPTY_FIELD_ERROR}}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = "form_control"
