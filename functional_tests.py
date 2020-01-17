from selenium import webdriver
from unittest import TestCase

import unittest

class NewVisitorTest(TestCase):

    def setUp(self):

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):

        self.browser.quit()

    # After going to the website, the visitor realized that title of website is “Reading books Tracker”.
    def test_can_start_test(self):

        self.browser.get('http://localhost:8000')
        self.assertIn('Reading tracker', self.browser.title)






        #  The visitor saw a header “Please enter a book’s title that you’d like to track, page number where you’re currently on and total page numbers of the book.”

        # Under the header, there are 3 input boxes.

        #  On the left, the longest input box is a textfield type to write book’s title down.

        # Next to title input box there are two square digits fields. On first of them, there is text “Your current page” and on the second one – “Book total page number”.

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
