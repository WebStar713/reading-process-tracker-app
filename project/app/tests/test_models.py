from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from app.models import Book, ListfOfBooks


class BookModelTest(TestCase):

    def test_default_book_details(self):
        book = Book()
        self.assertEqual([book.title, book.current_page, book.total_pages],
                         ['', None, None])

    def test_book_is_related_to_list_of_books(self):
        list_of_books = ListfOfBooks.objects.create()
        book = Book(list_of_books = list_of_books,
                    title = 'Some title',
                    current_page = 1,
                    total_pages = 255,)
        book.save()
        self.assertIn(book, list_of_books.book_set.all())

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

class ListfOfBooksModelTest(TestCase):

    def test_get_absolute_url(self):
        list_of_books = ListfOfBooks.objects.create()
        self.assertEqual(list_of_books.get_absolute_url(), '/lists/%d/' % (list_of_books.id))
