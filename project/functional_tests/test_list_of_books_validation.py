from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from urllib.parse import urljoin
from unittest import skip
from seleniumlogin import force_login
from django.contrib.auth import get_user_model

import unittest
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BookValidationTest(FunctionalTest):

    def test_1cannot_add_empty_book_details(self):

        # Uses had seen a login panel and logged in
        # (login has been tested in test_login.py)
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        force_login(user, webdriver.Chrome(), self.live_server_url)
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_password').send_keys('test12345')
        button_login_book = self.browser.find_element_by_class_name('button')
        button_login_book.click()

        # User tried to type empty value in input boxes
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()

        input_title_box.send_keys('')
        input_current_page_box.send_keys(34)
        input_total_pages_box.send_keys(45)
        button_add_book.click()

        # After that, user noticed info about lack possibility to type empty value
        error = self.browser.find_element_by_css_selector('.has-error').text
        self.assertEqual(error, "This field is required.")


        # User tried once again by entering whatever values into inbput boxes
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()

        input_title_box.send_keys("Secondhand: Travels in the New Global Garage Sale")
        input_current_page_box.send_keys(12)
        input_total_pages_box.send_keys(320)
        button_add_book.click()

        self.check_for_columns_in_book_table("Secondhand: Travels in the New Global Garage Sale", 12, 320)

        # User could fix empty input boxes by entering there some text
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()

        input_title_box.send_keys("1984")
        input_current_page_box.send_keys(10)
        input_total_pages_box.send_keys(237)
        button_add_book.click()

        self.check_for_columns_in_book_table("Secondhand: Travels in the New Global Garage Sale", 12, 320)
        self.check_for_columns_in_book_table("1984", 10, 237)

        # User logged out
        self.browser.find_element_by_link_text('Logout').click()

    def test_2cannot_add_duplicate_books(self):
        # User had gone to website and added first book
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        force_login(user, webdriver.Chrome(), self.live_server_url)
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_password').send_keys('test12345')
        button_login_book = self.browser.find_element_by_class_name('button')
        button_login_book.click()

        button_add_book = self.browser.find_element_by_class_name('button_add_book')
        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()

        input_title_box.send_keys("Fibonacci’s Rabbits")
        input_current_page_box.send_keys(10)
        input_total_pages_box.send_keys(176)
        button_add_book.click()

        self.check_for_columns_in_book_table("Fibonacci’s Rabbits", 10, 176)

        # After that, the user tried to type book that already occurs in a list
        button_add_book = self.browser.find_element_by_class_name('button_add_book')
        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()

        input_title_box.send_keys("Fibonacci’s Rabbits")
        input_current_page_box.send_keys(10)
        input_total_pages_box.send_keys(176)
        button_add_book.click()

        # The user received error message about potencial duplicated book
        self.check_for_columns_in_book_table("Fibonacci’s Rabbits", 10, 176)

        error = self.browser.find_element_by_css_selector('.has-error').text
        self.assertEqual(error, "This book is already on your list.")

        # User logged out
        self.browser.find_element_by_link_text('Logout').click()
