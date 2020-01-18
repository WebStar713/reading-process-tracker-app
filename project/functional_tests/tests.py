from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import TestCase

import unittest
import time

class NewVisitorTest(TestCase):

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

    def test_can_start_test(self):
        # After going to the website, the visitor realized that title of website
        # is “Reading books Tracker”.
        self.browser.get('http://localhost:8000')
        self.assertIn('Reading tracker', self.browser.title)

        # The visitor realized a header "Your books reading process"
        expected_header = "Your books reading progress"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(expected_header, header_text)

        # The visitor saw a text “Please enter a book’s title
        # that you’d like to track, page number where you’re currently on
        # and total page numbers of the book.”
        expected_instruction = "Please type a book’s title that you’d like to track, page number where you’re currently on and total page numbers of the book."
        instruction_text = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual(expected_instruction, instruction_text)

        # Under the header, there are 3 input boxes.
        #  On the left, the longest input box is a textfield type to write book’s title down.
        input_new_book_box = self.browser.find_element_by_id('id_new_book')
        self.assertEqual(input_new_book_box.get_attribute('placeholder'), 'Book\'s title')

        # Next to title input box there are two square digits fields.
        # On first of them, there is text “Your current page”
        # and on the second one – “Book total page number”.
        input_current_page_box = self.browser.find_element_by_id('id_current_page')
        self.assertEqual(input_current_page_box.get_attribute('placeholder'), 'Current page')

        input_total_pages_box = self.browser.find_element_by_id('id_total_pages')
        self.assertEqual(input_total_pages_box.get_attribute('placeholder'), 'Total pages in a book')

        # Below the input boxes, there is a button “Save and see a chart”.
        button_save_and_see_chart = self.browser.find_element_by_css_selector('.button_main')

        # The visitor is typying values in all three input boxes
        # After pressing button the user is redirecting to another site.
        input_new_book_box.send_keys('The Power of Habit')
        input_current_page_box.send_keys(129)
        input_total_pages_box.send_keys(371)
        button_save_and_see_chart.click()

        # On that site, the user is able to see table of last entered title
        self.check_for_columns_in_book_table('The Power of Habit', 129, 371)

        # Quick check if visitor is able to post second books details
        input_new_book_box = self.browser.find_element_by_id('id_new_book')
        input_current_page_box = self.browser.find_element_by_id('id_current_page')
        input_total_pages_box = self.browser.find_element_by_id('id_total_pages')
        button_save_and_see_chart = self.browser.find_element_by_css_selector('.button_main')

        input_new_book_box.send_keys('Factfulness')
        input_current_page_box.send_keys(0)
        input_total_pages_box.send_keys(341)
        button_save_and_see_chart.click()

        self.check_for_columns_in_book_table('Factfulness', 0, 341)

        # Check if details for both books saved
        self.check_for_columns_in_book_table('The Power of Habit', 129, 371)


        # ... and graph showing present progress.

        # Below there is a text “Please enter another book’s title” with analogous input boxes.

        # Below them, there are 2 buttons “Save and enter the next one” and “Save and see your cumulated chart”.

        #  After selecting “Save and enter the next one” 3 input boxes appeared.

            # Below them, there are 2 buttons “Save and enter the next one” and ““Save and see your cumulated chart” and so on…

        # After selecting “Save and see your charts” the website refreshed itself and showed chart.

           # On the charts the user is able to see all his books with reading progress assigned to them.
        #self.fail('End!')
if __name__ == "__main__":
    unittest.main()
