from django.db import models
from django.conf import settings
from django.utils.text import slugify

class ListfOfBooks(models.Model):
    pass


class Book(models.Model):
    title = models.TextField()
    current_page = models.IntegerField()
    total_pages = models.IntegerField()
    list_of_books = models.ForeignKey(ListfOfBooks, default=None, on_delete=models.PROTECT)
