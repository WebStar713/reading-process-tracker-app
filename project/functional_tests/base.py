from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import unittest

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    @classmethod
    def tearDown(self):
        self.browser.quit()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_columns_in_book_table(self, test_title, test_current_page, test_total_pages):
        table = self.browser.find_element_by_id('id_book_table')
        columns = table.find_elements_by_tag_name('td')
        self.assertIn(test_title, [column.text for column in columns])
        self.assertIn(str(test_current_page), [column.text for column in columns])
        self.assertIn(str(test_total_pages), [column.text for column in columns])

    def get_title_input_box(self):
        return self.browser.find_element_by_id('id_title')

    def get_current_page_input_box(self):
        return self.browser.find_element_by_id('id_current_page')

    def get_total_pages_input_box(self):
        return self.browser.find_element_by_id('id_total_pages')
