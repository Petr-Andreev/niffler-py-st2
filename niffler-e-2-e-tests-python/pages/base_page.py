from selene import browser


class BasePage:

    def open_url(self, url):
        browser.open(url)
