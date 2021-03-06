from .base import FunctionalTest
from selenium import webdriver
from seleniumlogin import force_login
from django.contrib.auth import get_user_model
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from urllib.parse import urljoin
from unittest import skip

import unittest
import time

class NewVisitorTest(FunctionalTest):

    def test_can_single_user_can_save_list(self):
        # After going to the website, the visitor realized that title of website
        # is “Reading books Tracker”.
        self.browser.get(self.live_server_url)
        self.assertIn('Reading tracker', self.browser.title)

        # The visitor realized a header "Your books reading process"
        expected_header = "Your books reading progress"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(expected_header, header_text)

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


        # The visitor saw a text “Please enter a book’s title
        # that you’d like to track, page number where you’re currently on
        # and total page numbers of the book.”
        expected_instruction = "Please type details of the book of which progress you'd like to track."
        instruction_text = self.browser.find_element_by_tag_name('h4').text
        self.assertEqual(expected_instruction, instruction_text)

        # Under the header, there are 3 input boxes.
        #  On the left, the longest input box is a textfield type to write book’s title down.
        input_title_box = self.get_title_input_box()
        self.assertEqual(input_title_box.get_attribute('placeholder'), 'Title')

        # Next to title input box there are two square digits fields.
        # On first of them, there is text “Your current page”
        # and on the second one – “Book total page number”.
        input_current_page_box = self.get_current_page_input_box()
        self.assertEqual(input_current_page_box.get_attribute('placeholder'), 'Current page')

        input_total_pages_box = self.get_total_pages_input_box()
        self.assertEqual(input_total_pages_box.get_attribute('placeholder'), 'Total number of pages')

        # Below the input boxes, there is a button “Save and see a chart”.
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        # The visitor is typying values in all three input boxes
        # After pressing button the user is redirecting to another site.
        input_title_box.send_keys('The Power of Habit')
        input_current_page_box.send_keys(129)
        input_total_pages_box.send_keys(371)
        button_add_book.click()

        # On that site, the user is able to see table of last entered title
        self.check_for_columns_in_book_table('The Power of Habit', 129, 371)

        # Quick check if visitor is able to post second books details
        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        input_title_box.send_keys('Factfulness')
        input_current_page_box.send_keys(0)
        input_total_pages_box.send_keys(341)
        button_add_book.click()


        self.check_for_columns_in_book_table('Factfulness', 0, 341)

        # Check if details for both books haved been saved
        self.check_for_columns_in_book_table('The Power of Habit', 129, 371)

        # User logged out
        self.browser.find_element_by_link_text('Logout').click()


    def test_can_multiple_users_can_save_list(self):
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        force_login(user, webdriver.Chrome(), self.live_server_url)
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_password').send_keys('test12345')
        button_login_book = self.browser.find_element_by_class_name('button')
        button_login_book.click()

        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        input_title_box.send_keys('The Power of Habit')
        input_current_page_box.send_keys(129)
        input_total_pages_box.send_keys(371)
        button_add_book.click()
        self.check_for_columns_in_book_table('The Power of Habit', 129, 371)

        # User logged out
        self.browser.find_element_by_link_text('Logout').click()
        self.browser.quit()

        # New user starts using the website
        self.browser = webdriver.Chrome()
        User = get_user_model()
        user = User.objects.create_user(username='usertest1', password='test123456')
        force_login(user, webdriver.Chrome(), self.live_server_url)
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest1')
        self.browser.find_element_by_id('id_password').send_keys('test123456')
        button_login_book = self.browser.find_element_by_class_name('button')
        button_login_book.click()

        # New user cannot see any lists of previous user
        previous_user_page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('The Power of Habit', previous_user_page_text)
        self.assertNotIn('Factfulness', previous_user_page_text)

        # New user is creating his own list of books
        input_title_box = self.get_title_input_box()
        input_current_page_box = self.get_current_page_input_box()
        input_total_pages_box = self.get_total_pages_input_box()
        button_add_book = self.browser.find_element_by_class_name('button_add_book')

        input_title_box.send_keys('You Look Like a Thing and I Love You')
        input_current_page_box.send_keys(1)
        input_total_pages_box.send_keys(272)
        button_add_book.click()


        # And check again if there is not a list of another user
        previous_user_page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('The Power of Habit', previous_user_page_text)
        # but we check if there is a list of our new user
        self.assertIn('You Look Like a Thing and I Love You', previous_user_page_text)

        # ... and graph showing present progress.
        chart = self.browser.find_element_by_id('bar-chart')
        self.assertTrue(chart)

        # User logged out
        self.browser.find_element_by_link_text('Logout').click()
