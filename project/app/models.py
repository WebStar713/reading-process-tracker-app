from django.db import models

class Book(models.Model):
    title = models.TextField()
    current_page = models.IntegerField()
    total_pages = models.IntegerField()
