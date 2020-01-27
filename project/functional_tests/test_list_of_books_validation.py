from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from urllib.parse import urljoin
from unittest import skip

import unittest
import time



class BookValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_book_details(self):
        pass
        # User tried to type empty value in input boxes

        # After that, user noticed info about lack possibility to type empty value

        # User tried once again by entering whatever values into inbput boxes


    # def test_user_cannot_sign_in_after_entering_invalid_data(self):
    #     url = urljoin(self.live_server_url, '/login/')
    #     self.browser.get(url)
    #
    #     # User goes to login page and realizes that the login form is there
    #     expected_login_header = "Login to account"
    #     login_header_text = self.browser.find_element_by_tag_name('h3').text
    #     self.assertEqual(expected_login_header, login_header_text)
    #
    #     # User enters invalid username and password and then receives info
    #     # about invalid login process
    #     input_login = self.browser.find_element_by_id('id_username')
    #     input_password = self.browser.find_element_by_id('id_password')
    #     button_login = self.browser.find_element_by_css_selector('.button_login')
    #
    #     input_login.send_keys('username')
    #     input_password.send_keys('password')
    #     button_login.click()
    #
    #     invalid_login_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertIn("Please enter a correct username and password", invalid_login_text)

    # def test_user_can_sign_in_after_entering_valid_data(self):
    #     url = urljoin(self.live_server_url, '/login/')
    #     self.browser.get(url)
    #
    #     # User enters valid username and password and then receives info
    #     # about successful login process
    #     input_login = self.browser.find_element_by_id('id_username')
    #     input_password = self.browser.find_element_by_id('id_password')
    #     button_login = self.browser.find_element_by_css_selector('.button_login')
    #
    #     input_login.send_keys('usernametest')
    #     input_password.send_keys('passwordtest')
    #     button_login.click()
    #
    #     time.sleep(10)
    #     valid_login_text = self.browser.find_element_by_tag_name('body').text
    #     #self.assertEqual(valid_login_text, 'Authenticated successfully')
