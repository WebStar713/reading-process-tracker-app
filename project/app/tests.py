from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.views import homePage
from app.models import Book

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_saves_POST_request(self):
        response = self.client.post('/', data={
                            'title': 'Some book',
                            'current_page': '125',
                            'total_pages': '317',
                            })
        self.assertIn('Some book', response.content.decode())
        self.assertIn('125', response.content.decode())
        self.assertIn('317', response.content.decode())

    def test_saves_and_retrieves_lots_books_details(self):
        first_book = Book()
        first_book.title = 'Title of first book'
        first_book.current_page = '12'
        first_book.total_pages = '300'
        first_book.save()

        second_book = Book()
        second_book.title = 'Title of second book'
        second_book.current_page = '70'
        second_book.total_pages = '566'
        second_book.save()

        saved_books = Book.objects.all()
        self.assertEqual(saved_books.count(), 2)

        first_saved_book = saved_books[0]
        second_saved_book = saved_books[1]
        self.assertEqual(first_saved_book.title, 'Title of first book')
        self.assertEqual(second_saved_book.title, 'Title of second book')
