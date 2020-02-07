from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.html import escape

from unittest import skip

from app.views import homePage
from app.models import Book, ListfOfBooks
from app.forms import (BookForm, ExisitingBooksInList, EMPTY_INPUT_ERROR,
                       DUPLICATE_INPUT_ERROR, DUPLICATE_USERS_ERROR,
                       UserRegistrationForm)


class HomePageTest(TestCase):

    def test_uses_base_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base.html')

    def test_homePage_uses_AuthenticationForm(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], AuthenticationForm)


class NewListTest(TestCase):

    def setUp(self):
        self.credentials = {'username': 'testuser',
                            'password': '12345test'}

        if not User.objects.filter(username='testuser').exists():
            self.user = User.objects.create_user(**self.credentials)
            self.user.save()
        else:
            self.user = User(username='testuser', password='12345test')

        self.logged_in = self.client.login(username='testuser', password='12345test')

    def test_saving_POST_request(self):
        self.client.post('/lists/new', data={
                            'title': 'Some book',
                            'current_page': 125,
                            'total_pages': 317,
                            })


        self.assertEqual(Book.objects.count(), 1)
        new_book = Book.objects.first()
        self.assertEqual(new_book.title, 'Some book')
        self.assertEqual(new_book.current_page, 125)
        self.assertEqual(new_book.total_pages, 317)

    def test_invalid_book_details_arent_saved(self):
        self.client.post('/lists/new', data={
                         'title': '', 'current_page': 125, 'total_pages': 317,})
        self.assertEqual(ListfOfBooks.objects.count(), 0)
        self.assertEqual(Book.objects.count(), 0)

    def test_for_invalid_input_renders_homePage_template(self):
        response = self.client.post('/lists/new', data={
                            'title': '',
                            'current_page': 125,
                            'total_pages': 317,
                            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_homePage(self):
        response = self.client.post('/lists/new', data={
                            'title': '',
                            'current_page': 125,
                            'total_pages': 317,
                            })

        self.assertContains(response, escape(EMPTY_INPUT_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={
                            'title': '',
                            'current_page': 125,
                            'total_pages': 317,
                            })

        self.assertIsInstance(response.context['form'], BookForm)

class ListViewTest(TestCase):

    def setUp(self):
        self.credentials = {'username': 'testuser',
                            'password': '12345test'}

        if not User.objects.filter(username='testuser').exists():
            self.user = User.objects.create_user(**self.credentials)
            self.user.save()
        else:
            self.user = User(username='testuser', password='12345test')

        self.client.login(username='testuser', password='12345test')

    def test_uses_list_template(self):
        list_of_books = ListfOfBooks.objects.create()
        response = self.client.get('/lists/%d/' % (list_of_books.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_of_books_to_template(self):
        other_list_of_books = ListfOfBooks.objects.create()
        correct_list_of_books = ListfOfBooks.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list_of_books.id,))
        self.assertEqual(response.context['list_of_books'], correct_list_of_books)

    def test_displays_only_books_for_that_list(self):
        correct_list_of_books = ListfOfBooks.objects.create()
        Book.objects.create(title = 'Title1',
                            current_page = 1,
                            total_pages = 111,
                            list_of_books = correct_list_of_books)
        other_list_of_books = ListfOfBooks.objects.create()
        Book.objects.create(title = 'Title2',
                            current_page = 2,
                            total_pages = 222,
                            list_of_books = correct_list_of_books)

        other_list_of_books = ListfOfBooks.objects.create()
        Book.objects.create(title = 'Other Title1',
                            current_page = 3,
                            total_pages = 333,
                            list_of_books = other_list_of_books)
        Book.objects.create(title = 'Other Title2',
                            current_page = 4,
                            total_pages = 444,
                            list_of_books = other_list_of_books)

        response = self.client.get('/lists/%d/' % (correct_list_of_books.id,))

        self.assertContains(response, 'Title1')
        self.assertContains(response, 'Title2')
        self.assertNotContains(response, 'Other Title1')
        self.assertNotContains(response, 'Other Title2')

    def test_cannot_save_empty_book_details(self):
        list_of_books = ListfOfBooks.objects.create()
        book = Book()
        book.title = "" # empty book detail (title)
        book.current_page = 6
        book.total_pages = 344
        book.list_of_books = list_of_books
        with self.assertRaises(ValidationError):
            book.save()
            book.full_clean() # fully checks empty value in TextField.
            # In case lack of eliciting of full_clean(), django would save empty
            # title value and would not raise an exception

    def test_displays_BookForm(self):
        list_of_books = ListfOfBooks.objects.create()
        response = self.client.get('/lists/%d/' % (list_of_books.id,))

        self.assertIsInstance(response.context['form'], ExisitingBooksInList)
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="current_page"')
        self.assertContains(response, 'name="total_pages"')

    def post_invalid_input(self):
        list_of_books = ListfOfBooks.objects.create()
        return self.client.post('/lists/%d/' % (list_of_books.id), data={
            'title': '', 'current_page': 56, 'total_pages': 317,})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()

        self.assertEqual(Book.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()

        self.assertIsInstance(response.context['form'], ExisitingBooksInList)

    def test_for_input_shows_error_on_page(self):
        response = self.post_invalid_input()

        self.assertContains(response, escape(EMPTY_INPUT_ERROR))

    def test_duplicate_book_validation_errors_end_up_on_lists_page(self):
        list_of_books = ListfOfBooks.objects.create()
        book1 = Book.objects.create(list_of_books = list_of_books,
                                    title = 'Some title',
                                    current_page = 23,
                                    total_pages = 455,)
        response = self.client.post('/lists/%d/' % (list_of_books.id,),
                                    data = {'title' : 'Some title',
                                            'current_page' : 23,
                                            'total_pages' : 455,})

        expected_error = escape(DUPLICATE_INPUT_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Book.objects.all().count(), 1)

    def test_delete_added_books(self):
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        Client().force_login(user)

        self.client.get('/mylist/')
        list_of_books = ListfOfBooks.objects.create()
        book = Book.objects.create(list_of_books = list_of_books,
                                         title = 'Some title',
                                         current_page = 23,
                                         total_pages = 455,)

        self.assertEqual(Book.objects.all().count(), 1)

        self.client.post(reverse('bookDelete', kwargs={'pk': book.id}))
        self.assertEqual(Book.objects.all().count(), 0)


class RegisterTest(TestCase):

    def test_uses_register_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'register.html')

    def test_register_uses_UserRegistrationForm(self):
        response = self.client.get('/register/')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_saving_POST_request(self):
        self.client.post(reverse('register'), data={
                            'username': 'usertest',
                            'first_name': 'Anna',
                            'email': 'user@test.pl',
                            'password1': 'password123P()',
                            'password2': 'password123P()',
                            })


        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'usertest')
        self.assertEqual(new_user.first_name, 'Anna')
        self.assertEqual(new_user.email, 'user@test.pl')
        check_password(new_user.password, 'password123P()')

    def test_invalid_registration_inputs_arent_saved(self):

        # invalid email
        self.client.post(reverse('register'), data={
                            'username': 'usertest',
                            'first_name': 'Anna',
                            'email': 'usertest.pl',
                            'password1': 'password123P()',
                            'password2': 'password123P()',
                            })

        self.assertEqual(User.objects.count(), 0)

        # invalid username
        self.client.post(reverse('register'), data={
                            'username': '',
                            'first_name': 'Anna',
                            'email': 'user@test.pl',
                            'password1': 'password123P()',
                            'password2': 'password123P()',
                            })

        self.assertEqual(User.objects.count(), 0)

        # invalid first_name
        self.client.post(reverse('register'), data={
                            'username': 'usertest',
                            'first_name': '',
                            'email': 'user@test.pl',
                            'password': 'password123P()',
                            'password2': 'password123P()',
                            })

        self.assertEqual(User.objects.count(), 0)

        # invalid password1 (too short)
        self.client.post(reverse('register'), data={
                            'username': 'usertest',
                            'first_name': 'Anna',
                            'email': 'user@test.pl',
                            'password1': '123',
                            'password2': '123',
                            })

        self.assertEqual(User.objects.count(), 0)

        # not matching passwords
        self.client.post(reverse('register'), data={
                            'username': 'usertest',
                            'first_name': 'Anna',
                            'email': 'user@test.pl',
                            'password1': 'password123P()',
                            'password2': 'password123p()',
                            })

        self.assertEqual(User.objects.count(), 0)

    def test_validation_errors_are_shown_on_register_page(self):
        response = self.client.post(reverse('register'), data={
                            'username': '',
                            'first_name': 'Anna',
                            'email': 'user@test.pl',
                            'password1': 'password123P()',
                            'password2': 'password123P()',
                            })

        self.assertContains(response, escape(EMPTY_INPUT_ERROR))

    def test_duplicate_users_validation_errors(self):
        self.credentials = {'username': 'testuser',
                            'password': '12345test'}
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()

        response = self.client.post(reverse('register'), data={
                            'username': 'testuser',
                            'first_name': 'Anna',
                            'email': 'user@test.pl',
                            'password1': 'password123P()',
                            'password2': 'password123P()',
                            })

        expected_error = escape(DUPLICATE_USERS_ERROR)
        self.assertContains(response, expected_error)
        self.assertEqual(User.objects.all().count(), 1)

    def test_displays_UserRegistrationForm(self):
        response = self.client.get(reverse('register'))

        self.assertIsInstance(response.context['form'], UserRegistrationForm)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')
