from selene import browser, have, be

from pages.base_page import BasePage


class AuthPage(BasePage):
    def __init__(self):
        self.register_form = browser.element('.form__register')
        self.input_username = browser.element('input[name=username]')
        self.input_password = browser.element('input[name=password]')
        self.input_password_submit = browser.element('input[name=passwordSubmit]')
        self.button_submit = browser.element('button[type=submit]')
        self.congratulations_text = browser.element('.form__paragraph')
        self.form_sign_in = browser.element('.form_sign-in')

    def registration_form(self, username, password, url, congratulations_text):
        self.open_url(url)
        self.register_form.click()
        self.input_username.set_value(username)
        self.input_password.set_value(password)
        self.input_password_submit.set_value(password)
        self.button_submit.click()
        self.congratulations_text.should(have.text(congratulations_text))
        self.form_sign_in.should(be.visible).should(be.clickable)

    def aurh_form(self, url, username=None, password=None):
        self.open_url(url)
        self.input_username.set_value(username)
        self.input_password.set_value(password)
        self.button_submit.click()


registration_page = AuthPage()
auth_page = AuthPage()
