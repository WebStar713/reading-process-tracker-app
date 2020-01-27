from django.test import TestCase
from app.forms import BookForm

class BookFormTest(TestCase):

    def test_form_renders_BookForm_fields_input(self):
        form = BookForm()
        self.fail(form.as_p())
