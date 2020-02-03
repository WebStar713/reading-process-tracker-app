from .base import FunctionalTest
from seleniumlogin import force_login
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from private import STAFF_EMAIL

import time

class LoginTest(FunctionalTest):

    def test_login_on_home_page(self):
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        force_login(user, webdriver.Chrome(), self.live_server_url)

        # User goes to the website and realizes login form.
        # Enters correct data in login form and is redirecting to /mylist/ subpage
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_password').send_keys('test12345')
        button_login_book = self.browser.find_element_by_css_selector('.button_login')

        button_login_book.click()

        # User is able to see that he has been logged in
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hello ' + user.username, body)

class ForgottenPasswordTest(FunctionalTest):

    def test_forgotten_password_form_on_home_page_valid_data(self):
        # User realizes that home page contains "Forgotten your password?" form
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Forgotten your password?', body)

        self.browser.find_element_by_link_text('Forgotten your password?').click()

        # On the subpage where user can restart his password,
        # there is a window for typing email
        # User types his email and clicks on button
        email = self.browser.find_element_by_id('id_email').send_keys(STAFF_EMAIL)

        button_password_book = self.browser.find_element_by_css_selector('.button_login')
        button_password_book.click()

        # After that user sees information about successful reset process
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Instruction to set a new password has been e-mailed to your e-mail address.', body)

    
