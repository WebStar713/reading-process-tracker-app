from django import forms

from app.models import Book

class BookForm(forms.Form):
    title_text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'form-control input-lg',
        }),
    )
    current_page_int = forms.IntegerField(
        widget=forms.fields.NumberInput(attrs={
            'placeholder': 'Current page',
            'class': 'form-control input-lg',
        }),
    )
    total_page_int = forms.IntegerField(
        widget=forms.fields.NumberInput(attrs={
            'placeholder': 'Total number of pages',
            'class': 'form-control input-lg',
        }),
    )

    class Meta:
        model = Book
        fields = ['title', 'current_page', 'total_pages']
