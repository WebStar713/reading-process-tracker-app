from django.test import TestCase
from django.urls import resolve
from app.views import homePage

class HomePageTest(TestCase):

    def test_root_urls_resolves_to_HomePage_view(self):
        url_address = resolve('/')
        self.assertEqual(url_address.func, homePage)
