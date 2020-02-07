from .base import FunctionalTest
from django.contrib.auth import get_user_model
from django.test import Client
from selenium import webdriver
from unittest import skip

from private import STAFF_EMAIL

import time

class LoginTest(FunctionalTest):

    def test_1login_on_home_page(self):
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        Client().force_login(user)

        # User goes to the website and realizes login form.
        # Enters correct data in login form and is redirecting to /mylist/ subpage
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_password').send_keys('test12345')
        button_login_book = self.browser.find_element_by_class_name('button')

        button_login_book.click()

        # User is able to see that he has been logged in
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hello', body)

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

    def test_2forgotten_password_form_on_home_page_valid_data(self):
        # User realizes that home page contains "Forgotten your password?" form
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Forgotten your password?', body)

        self.browser.find_element_by_link_text('Forgotten your password?').click()

        # On the subpage where user can restart his password,
        # there is a window for typing email
        # User types his email and clicks on button
        email = self.browser.find_element_by_id('id_email').send_keys(STAFF_EMAIL)

        button_send_email = self.browser.find_element_by_class_name('button')
        button_send_email.click()

        # After that user sees information about successful reset process
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Instruction to set a new password has been e-mailed to your e-mail address.', body)

    @skip
    def test_3forgotten_password_form_on_home_page_invalid_data(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Forgotten your password?', body)
        self.browser.find_element_by_link_text('Forgotten your password?').click()

        # User is typing invalid email
        email = self.browser.find_element_by_id('id_email').send_keys('invalidemail.com')
        self.browser.find_element_by_class_name('button').click()

        # After that user sees information about failed reset process

        # how to find popup error message?

class RegistrationTest(FunctionalTest):

    def test_4user_can_register(self):
        # User notices link for creation account and clicks on it
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Create an account here.', body)
        self.browser.find_element_by_link_text('Create an account here.').click()

        # After it, he had been redirected for registration page
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Create an account', body)

        # User realizes registration form that contains:
        # usename, first name, email, password and password confirmation
        # Visitor tries to type his inputs in this form and clicks on button
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_first_name').send_keys('User')
        self.browser.find_element_by_id('id_email').send_keys(STAFF_EMAIL)
        self.browser.find_element_by_id('id_password1').send_keys('test12345')
        self.browser.find_element_by_id('id_password2').send_keys('test12345')

        button_create_account = self.browser.find_element_by_class_name('button')
        button_create_account.click()

        # After that, user had been redirected to page
        # confirming successful registration on which there is welcoming text
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome User!', body)
        self.assertIn('Thank you taking time to register. Your account has been successfully created.', body)
        self.assertIn('We hope you will enjoy our Reading Process Tracker.', body)

        # User sees link for login process
        login_link = self.browser.find_element_by_link_text('login').text
        self.assertIn('login', login_link)

        # After clicking on 'login' link the user is redirecting on login subpage
        self.browser.find_element_by_link_text('login').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Login to account', body) # login form had been testes earlier

class ChangePasswordTest(FunctionalTest):

    def test_5login_on_home_page(self):
        User = get_user_model()
        user = User.objects.create_user(username='usertest', password='test12345')
        Client().force_login(user)

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('usertest')
        self.browser.find_element_by_id('id_password').send_keys('test12345')
        button_login_book = self.browser.find_element_by_class_name('button')
        button_login_book.click()

        # User noticed link for password change
        password_change_link = self.browser.find_element_by_link_text('Change your password').text
        self.assertIn('Change your password', password_change_link)

        # After clicking on 'Change your password' link
        # the user is redirecting on "change your password" subpage
        self.browser.find_element_by_link_text('Change your password').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Use the form below to change your password.', body)

        # User noticed form for password change that contains:
        # old password, new password and confirmation for new password
        # User is filling them:
        self.browser.find_element_by_id('id_old_password').send_keys('test12345')
        self.browser.find_element_by_id('id_new_password1').send_keys('newtest12345')
        self.browser.find_element_by_id('id_new_password2').send_keys('newtest12345')

        button_change = self.browser.find_element_by_class_name('button')
        button_change.click()

        # User sees confirmation about successful password change
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Your password has been successfully changed.', body)
