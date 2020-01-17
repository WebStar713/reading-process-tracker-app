from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from app.views import homePage

class HomePageTest(TestCase):

    def test_root_urls_resolves_to_homePage_view(self):
        url_address = resolve('/')
        self.assertEqual(url_address.func, homePage)

    def test_homePage_returns_correct_html(self):
        request = HttpRequest()
        response = homePage(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
