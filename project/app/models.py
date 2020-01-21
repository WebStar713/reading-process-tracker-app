from django.db import models

class ListfOfBooks(models.Model):
    pass

class Book(models.Model):
    title = models.TextField(default='')
    current_page = models.IntegerField(default=0)
    total_pages = models.IntegerField(default=0)
    list_of_books = models.TextField(default='')
