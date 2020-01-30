from django.contrib import admin

from .models import Book

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'list_of_books_id')
