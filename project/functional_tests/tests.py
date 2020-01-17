from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        button_save_and_see_chart = self.browser.find_element_by_tag_name('button')

        # The visitor is typying values in all three input boxes
        input_new_book_box.send_keys('The Power of Habit')
        input_current_page_box.send_keys(129)
        input_total_pages_box.send_keys(371)

        # After pressing ENTER the visitor realized table with his book's title.
        # TODO: After pressing ENTER key is redirecting to another site.)
        # TODO: After pressing button the user is redirecting to another site.
        input_new_book_box.send_keys(Keys.ENTER)
        input_current_page_box.send_keys(Keys.ENTER)
        input_total_pages_box.send_keys(Keys.ENTER)


        # On that site, the user is able to see table of last entered title
        table = self.browser.find_element_by_id('id_book_table')
        rows = table.find_elements_by_id('tr')
        self.assertTrue(any(row.text == 'The Power of Habit' for row in rows))

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
