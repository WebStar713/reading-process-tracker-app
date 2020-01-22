from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.views import homePage
from app.models import Book, ListfOfBooks
from app.forms import LoginForm

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_of_books = ListfOfBooks.objects.create()
        response = self.client.get('/lists/%d/' % (list_of_books.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_books_for_that_list(self):
        correct_list_of_books = ListfOfBooks.objects.create()
        Book.objects.create(title = 'Title1',
                            current_page = 1,
                            total_pages = 111,
                            list_of_books = correct_list_of_books)
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

    def test_saving_POST_request(self):
        response = self.client.post('/lists/new', data={
                            'title': 'Some book',
                            'current_page': 125,
                            'total_pages': 317,
                            })

        self.assertEqual(Book.objects.count(), 1)
        new_book = Book.objects.first()
        self.assertEqual(new_book.title, 'Some book')
        self.assertEqual(new_book.current_page, 125)
        self.assertEqual(new_book.total_pages, 317)


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={
                            'title': 'Some book',
                            'current_page': 125,
                            'total_pages': 317,
                            })

        new_list_of_books = ListfOfBooks.objects.first()
        self.assertRedirects(response, f'/lists/{new_list_of_books.id}/')


    def test_passes_correct_list_of_books_to_template(self):
        correct_list_of_books = ListfOfBooks.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list_of_books.id,))
        self.assertEqual(response.context['list_of_books'], correct_list_of_books)

class ListfOfBooksAndBookModelTest(TestCase):

    def test_saves_and_retrieves_lots_books_details(self):
        list_of_books = ListfOfBooks()
        list_of_books.save()

        first_book = Book()
        first_book.title = 'Title of first book'
        first_book.current_page = 12
        first_book.total_pages = 300
        first_book.list_of_books = list_of_books
        first_book.save()

        second_book = Book()
        second_book.title = 'Title of second book'
        second_book.current_page = 70
        second_book.total_pages = 566
        second_book.list_of_books = list_of_books
        second_book.save()

        saved_list_of_books = ListfOfBooks.objects.first()
        self.assertEqual(saved_list_of_books, list_of_books)

        saved_books = Book.objects.all()
        self.assertEqual(saved_books.count(), 2)

        first_saved_book = saved_books[0]
        second_saved_book = saved_books[1]
        self.assertEqual(first_saved_book.title, 'Title of first book')
        self.assertEqual(first_saved_book.list_of_books, list_of_books)
        self.assertEqual(second_saved_book.title, 'Title of second book')
        self.assertEqual(second_saved_book.list_of_books, list_of_books)

class NewBookTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list_of_books = ListfOfBooks.objects.create()

        self.client.post('/lists/%d/add_book' % (correct_list_of_books.id,),
                        data={'title': 'New book title for existing list',
                              'current_page': 100,
                              'total_pages': 312,})

        self.assertEqual(Book.objects.count(), 1)
        new_book = Book.objects.first()
        self.assertEqual(new_book.title, 'New book title for existing list')
        self.assertEqual(new_book.current_page, 100)
        self.assertEqual(new_book.total_pages, 312)
        self.assertEqual(new_book.list_of_books, correct_list_of_books)

    def test_redirects_to_list_view(self):
        correct_list_of_books = ListfOfBooks.objects.create()

        response = self.client.post('/lists/%d/add_book' % (correct_list_of_books.id,),
                        data={'title': 'New book title for existing list',
                              'current_page': 100,
                              'total_pages': 312,})

        self.assertRedirects(response, f'/lists/{correct_list_of_books.id}/')

class LoginTest(TestCase):
    def test_uses_login_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')

    def test_form_validation_for_blank_login_inputs(self):
        EMPTY_FIELD_ERROR = 'This field is required.'
        form = LoginForm(data={'username': '', 'password': '',})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [EMPTY_FIELD_ERROR])

    # def test_form_validation(self):
    #     form = LoginForm({'username': 'Username1', 'password': 'Password1',})
    #
    #     saved_form = form.save()
    #     self.assertEqual(saved_form.username, 'Username1')
    #     self.assertEqual(saved_form.password, 'Password1')
