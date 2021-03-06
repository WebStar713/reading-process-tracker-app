from django.test import TestCase, Client
from django.contrib.auth.models import User
from app.forms import (BookForm, ExisitingBooksInList, UserRegistrationForm,
                      EMPTY_INPUT_ERROR, DUPLICATE_INPUT_ERROR)
from app.models import ListfOfBooks, Book

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
        self.assertEqual(form.errors['title'], [EMPTY_INPUT_ERROR])

        form = BookForm(data={'title':'Some title', 'current_page': '', 'total_pages': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_page'], [EMPTY_INPUT_ERROR])

        form = BookForm(data={'title':'Some title', 'current_page': 20, 'total_pages': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['total_pages'], [EMPTY_INPUT_ERROR])

    def test_BookForm_handles_saving_to_a_ListOfBooks(self):
        list_of_books = ListfOfBooks.objects.create()
        form = BookForm(data={'title':'Some title', 'current_page': 11, 'total_pages': 56, })
        new_book = form.save(for_list=list_of_books)

        self.assertEqual(new_book, Book.objects.first())
        self.assertEqual(new_book.title, 'Some title')
        self.assertEqual(new_book.list_of_books, list_of_books)

class ExisitingBooksInListTest(TestCase):

    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create(username='testuser')
        user.set_password('12345test')
        user.save()
    else:
        user = User(username='testuser', password='12345test')

    Client().login(username='testuser', password='12345test')

    def test_form_renders_BookForm_fields_input(self):

        list_of_books = ListfOfBooks.objects.create()
        form = ExisitingBooksInList(for_list = list_of_books, owner = self.user)

        self.assertIn('placeholder="Title"', form.as_p())
        self.assertIn('placeholder="Current page"', form.as_p())
        self.assertIn('placeholder="Total number of pages"', form.as_p())

    def test_validation_for_blank_inputs(self):
        list_of_books = ListfOfBooks.objects.create()
        form = ExisitingBooksInList(for_list = list_of_books, data={
                        'title':'',
                        'current_page': 45,
                        'total_pages': 500, }, owner=self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [EMPTY_INPUT_ERROR])

        form = ExisitingBooksInList(for_list = list_of_books, data={
                        'title':'Some title',
                        'current_page': '',
                        'total_pages': 500, }, owner=self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_page'], [EMPTY_INPUT_ERROR])

        form = ExisitingBooksInList(for_list = list_of_books, data={
                        'title':'Some title',
                        'current_page': 45,
                        'total_pages': '', }, owner=self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['total_pages'], [EMPTY_INPUT_ERROR])

    def test_form_validation_for_duplicate_books(self):
        list_of_books = ListfOfBooks.objects.create()
        Book.objects.create(list_of_books = list_of_books,
                            title = 'No duplicates!',
                            current_page = 23,
                            total_pages = 600,)

        form = ExisitingBooksInList(for_list = list_of_books, data={
                        'title':'No duplicates!',
                        'current_page': 23,
                        'total_pages': 600,}, owner = self.user)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [DUPLICATE_INPUT_ERROR])

    def test_form_save(self):
        list_of_books = ListfOfBooks.objects.create()
        form = ExisitingBooksInList(for_list = list_of_books, data={
                        'title':'Some tite',
                        'current_page': 231,
                        'total_pages': 677,}, owner = self.user)
        new_book = form.save()
        self.assertEqual(new_book, Book.objects.all()[0])

class UserRegistrationFormTest(TestCase):
    def test_form_renders_UserRegistrationForm_fields_input(self):
        form = UserRegistrationForm()

        self.assertIn('Username', form.as_p())
        self.assertIn('First name', form.as_p())
        self.assertIn('Password', form.as_p())
        self.assertIn('Password confirmation', form.as_p())
        self.assertIn('Email', form.as_p())

    def test_validation_for_blank_user_inputs(self):
        form = UserRegistrationForm(data={'username':'',
                                          'first_name': '',
                                          'password1': '',
                                          'password2':'',
                                          'email': '',
                                          })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [EMPTY_INPUT_ERROR])
        self.assertEqual(form.errors['first_name'], [EMPTY_INPUT_ERROR])
        self.assertEqual(form.errors['email'], [EMPTY_INPUT_ERROR])
        self.assertEqual(form.errors['password1'], [EMPTY_INPUT_ERROR])
        self.assertEqual(form.errors['password2'], [EMPTY_INPUT_ERROR])
