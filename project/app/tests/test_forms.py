from django.test import TestCase
from app.forms import BookForm

class BookFormTest(TestCase):

    def test_form_renders_BookForm_fields_input(self):
        form = BookForm()

        self.assertIn('placeholder="Title"', form.as_p())
        self.assertIn('placeholder="Current page"', form.as_p())
        self.assertIn('placeholder="Total number of pages"', form.as_p())

        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_validation_for_blank_book_details_input(self):
        form = BookForm(data={'title':'', 'current_page': 45, 'total_pages': 500, })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ['These fields cannot be blank.'])

        form = BookForm(data={'title':'Some title', 'current_page': '', 'total_pages': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_page'], ['These fields cannot be blank.'])

        form = BookForm(data={'title':'Some title', 'current_page': 20, 'total_pages': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['total_pages'], ['These fields cannot be blank.'])
