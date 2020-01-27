from django.test import TestCase
from django.core.urlresolvers import reverse


from app.models import Book, ListfOfBooks


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

    def test_get_absolute_url(self):
        list_of_books = ListfOfBooks.objects.create()
        self.assertEqual(list_of_books.get_absolute_url(), '/lists/%d' % (list_of_books.id))
