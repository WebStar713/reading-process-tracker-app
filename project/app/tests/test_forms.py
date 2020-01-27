from django.test import TestCase
from app.forms import BookForm

class BookFormTest(TestCase):
    form = BookForm()
    self.fail(form.as_p())
