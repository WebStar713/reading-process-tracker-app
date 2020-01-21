from django.db import models

class Book(models.Model):
    title = models.TextField(default='')
    current_page = models.IntegerField(default=0)
    total_pages = models.IntegerField(default=0)

class ListfOfBooks(models.Model):
    pass
