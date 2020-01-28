from django import forms
from django.core.exceptions import ValidationError

from app.models import Book, ListfOfBooks

EMPTY_INPUT_ERROR = 'These fields cannot be blank.'
DUPLICATE_INPUT_ERROR = 'This book is already on your list.'

class BookForm(forms.models.ModelForm):

    class Meta:
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

    def save(self, for_list):
        self.instance.list_of_books = for_list
        return super().save()

class ExisitingBooksInList(BookForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list_of_books = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as error:
            error.error_dict = {'title': [DUPLICATE_INPUT_ERROR]}
            self._update_errors(error)

    def save(self):
        return forms.models.ModelForm.save(self)
