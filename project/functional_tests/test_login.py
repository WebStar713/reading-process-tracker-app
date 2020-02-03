from .base import FunctionalTest

class LoginTest(FunctionalTest):

    def test_login_on_home_page(self):

        # User goes to the website and realizes login form.
        # Enters correct data in login form and is redirecting to /mylist/ subpage
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_username').send_keys('testuser')
        self.browser.find_element_by_id('id_password').send_keys('12345test')
        button_login_book = self.browser.find_element_by_css_selector('.button_login')

        button_login_book.click()
