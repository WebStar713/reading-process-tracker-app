from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.views import homePage
from app.models import Book, ListfOfBooks

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/first-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_books_details(self):
        Book.objects.create(title = 'Title1',
                            current_page = 1,
                            total_pages = 111,)
        Book.objects.create(title = 'Title2',
                            current_page = 2,
                            total_pages = 222,)
        response = self.client.get('/lists/first-list/')
        self.assertContains(response, 'Title1')
        self.assertContains(response, 'Title2')

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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/first-list/')



class ListAndBookModelTest(TestCase):

    def test_saves_and_retrieves_lots_books_details(self):
        list_of_books = ListfOfBooks()
        list_of_books.save()

        first_book = Book()
        first_book.title = 'Title of first book'
        first_book.current_page = 12
        first_book.total_pages = 300
        first_book.list = list_of_books
        first_book.save()

        second_book = Book()
        second_book.title = 'Title of second book'
        second_book.current_page = 70
        second_book.total_pages = 566
        second_book.list = list_of_books
        second_book.save()

        saved_list_of_books = ListfOfBooks.object.first()
        self.assertEqual(saved_list_of_books, list_of_books)

        saved_books = Book.objects.all()
        self.assertEqual(saved_books.count(), 2)

        first_saved_book = saved_books[0]
        second_saved_book = saved_books[1]
        self.assertEqual(first_saved_book.title, 'Title of first book')
        self.assertEqual(first_saved_book.list, list_of_books)
        self.assertEqual(second_saved_book.title, 'Title of second book')
        self.assertEqual(second_saved_book.list, list_of_books)
