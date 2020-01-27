from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import escape

from app.views import homePage
from app.models import Book, ListfOfBooks


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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={
                            'title': '',
                            'current_page': 125,
                            'total_pages': 317,
                            })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("These fields cannot be blank.")
        self.assertContains(response, expected_error)
