from selenium import webdriver
from unittest import TestCase

import unittest

class NewVisitorTest(TestCase):

    def setUp(self):

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):

        self.browser.quit()


    def test_can_start_test(self):

        # After going to the website, the visitor realized that title of website
        # is “Reading books Tracker”.
        self.browser.get('http://localhost:8000')
        self.assertIn('Reading tracker', self.browser.title)

        # The visitor realized a header "Your books reading process"
        expected_header = "Your books reading process"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(expected_header, header_text)

        # The visitor saw a text “Please enter a book’s title
        # that you’d like to track, page number where you’re currently on
        # and total page numbers of the book.”
        expected_instruction = "Please enter a book’s title that you’d like to track, page number where you’re currently on and total page numbers of the book."
        instruction_text = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual(expected_instruction, instruction_text)

        # Under the header, there are 3 input boxes.
        #  On the left, the longest input box is a textfield type to write book’s title down.
        input_new_book_box = self.browser.find_element_by_id('new_book')
        self.assertEqual(input_new_book_box.get_attribute('placeholder'), 'Book\'s title')

        # Next to title input box there are two square digits fields.
        # On first of them, there is text “Your current page”
        # and on the second one – “Book total page number”.
        input_current_page_box = self.browser.find_element_by_id('current_page')
        self.assertEqual(input_current_page_box.get_attribute('placeholder'), 'Current page')

        input_total_pages_box = self.browser.find_element_by_id('total_pages')
        self.assertEqual(input_total_pages_box.get_attribute('placeholder'), 'Total pages in a book')

        # Below the input boxes, there is a button “Save and see a chart”.

        # After pressing it / and after pressing ENTER key, the user is redirecting to another site.

        # On that site, the user is able to see graph showing present progress.

        # Below there is a text “Please enter another book’s title” with analogous input boxes.

        # Below them, there are 2 buttons “Save and enter the next one” and “Save and see your cumulated chart”.

        #  After selecting “Save and enter the next one” 3 input boxes appeared.

            # Below them, there are 2 buttons “Save and enter the next one” and ““Save and see your cumulated chart” and so on…

        # After selecting “Save and see your charts” the website refreshed itself and showed chart.

           # On the charts the user is able to see all his books with reading progress assigned to them.
        #self.fail('End!')
if __name__ == "__main__":
    unittest.main()
