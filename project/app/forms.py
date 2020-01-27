from django import forms

from app.models import Book

class BookForm(forms.models.ModelForm):

    class Meta:
        EMPTY_INPUT_ERROR = 'These fields cannot be blank.'
        model = Book
        fields = ['title', 'current_page', 'total_pages', ]
        widgets = {
        'title': forms.fields.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'form-control input-lg',
        }),
        'current_page': forms.fields.NumberInput(attrs={
            'placeholder': 'Current page',
            'class': 'form-control input-lg',
        }),
        'total_pages': forms.fields.NumberInput(attrs={
            'placeholder': 'Total number of pages',
            'class': 'form-control input-lg',
        }),
        }
        error_messages = {
        'title': {'required': EMPTY_INPUT_ERROR},
        'current_page': {'required': EMPTY_INPUT_ERROR},
        'total_pages': {'required': EMPTY_INPUT_ERROR},
        }
