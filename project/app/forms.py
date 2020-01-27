from django import forms

from django.contrib.auth.models import User

from app.models import Book, ListfOfBooks


class BookForm(forms.models.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'current_page', 'total_pages')
        widgets = {
            'title': forms.fields.TextInput(),
            'current_page': forms.fields.NumberInput(),
            'total_pages': forms.fields.NumberInput(),
        }



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form_control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form_control"}))

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    class Meta:
        EMPTY_FIELD_ERROR = 'This field is required.'
        model = User
        fields = ('username', 'password', 'first_name', 'email')

        error_messages = {'username': {'required': EMPTY_FIELD_ERROR}}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = "form_control"

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']
