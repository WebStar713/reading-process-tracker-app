from .base import FunctionalTest
from seleniumlogin import force_login
from django.contrib.auth import get_user_model
from selenium import webdriver
from unittest import skip

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

        # User also sees link for logout process
        logout_link = self.browser.find_element_by_link_text('Logout').text
        self.assertIn('Logout', logout_link)

        # After clicking on 'Logout' link the user is redirecting on logout subpage
        self.browser.find_element_by_link_text('Logout').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('You have been successfully logged out', body)

        # On logout subpage the user realizes 'login again' link and decides to click on it
        login_again_link = self.browser.find_element_by_link_text('login again').text
        self.assertEqual('login again', login_again_link)
        self.browser.find_element_by_link_text('login again').click()

        # User has been redirected to login subpage that contains username and password form
        self.browser.find_element_by_id('id_username')
        self.browser.find_element_by_id('id_password')



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

        button_send_email = self.browser.find_element_by_css_selector('.button_send')
        button_send_email.click()

        # After that user sees information about successful reset process
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Instruction to set a new password has been e-mailed to your e-mail address.', body)

    @skip
    def test_forgotten_password_form_on_home_page_invalid_data(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Forgotten your password?', body)
        self.browser.find_element_by_link_text('Forgotten your password?').click()

        # User is typing invalid email
        email = self.browser.find_element_by_id('id_email').send_keys('invalidemail.com')
        self.browser.find_element_by_css_selector('.button_send').click()

        # After that user sees information about failed reset process

        # how to find popup error message?
