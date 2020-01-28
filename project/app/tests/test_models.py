from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

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
        self.assertEqual(list_of_books.get_absolute_url(), '/lists/%d/' % (list_of_books.id))

    def test_duplicate_books_are_invalid(self):
        list_of_books = ListfOfBooks.objects.create()
        Book.objects.create(list_of_books = list_of_books,
                            title = 'Duplicate',
                            current_page = 10,
                            total_pages = 25,)

        with self.assertRaises(ValidationError):
            book = Book(list_of_books = list_of_books,
                        title = 'Duplicate',
                        current_page = 10,
                        total_pages = 25,)
            book.full_clean()

    def test_can_save_the_same_book_to_different_list(self):
        list_of_books_first = ListfOfBooks.objects.create()
        list_of_books_second = ListfOfBooks.objects.create()
        Book.objects.create(list_of_books = list_of_books_first,
                    title = 'Duplicate',
                    current_page = 10,
                    total_pages = 25,)
        book = Book(list_of_books = list_of_books_second,
                    title = 'Duplicate',
                    current_page = 10,
                    total_pages = 25,)
        book.full_clean()
