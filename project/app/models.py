from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class ListfOfBooks(models.Model):
    def get_absolute_url(self):
        return reverse('viewList', args=[self.id])


class Book(models.Model):
    title = models.TextField(blank=False)
    current_page = models.IntegerField(blank=False)
    total_pages = models.IntegerField(blank=False)
    list_of_books = models.ForeignKey(ListfOfBooks, default=None, on_delete=models.SET_DEFAULT)
