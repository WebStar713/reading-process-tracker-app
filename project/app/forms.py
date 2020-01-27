from django import forms

class BookForm(forms.Form):
    title_text = forms.CharField()
    current_page_int = forms.IntegerField()
    total_page_int = forms.IntegerField()
