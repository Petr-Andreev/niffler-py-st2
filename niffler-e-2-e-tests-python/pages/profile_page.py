from selene import browser, have, be

from pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self):
        self.profile_title = browser.element('[class="MuiTypography-root MuiTypography-h5 css-w1t7b3"]')
        self.categories_title = browser.element('[class ="MuiTypography-root MuiTypography-h5 css-1pam1gy"]')
        self.categories_name = lambda name_category: browser.element(f'//span[.="{name_category}"]')
        self.user_name = browser.element('#username')
        self.name = browser.element('#name')
        self.profile_button = browser.element('//*[@id="root"]/header/div/div[2]/button/span')
        self.search_category = browser.element('#category')
        self.image_profile = browser.element('.MuiBox-root.css-1cv8jtj')
        self.menu_categories = browser.element(
            '[class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-3w20vr"]')

    def title_form(self, profile=None, categories=None):
        self.profile_title.should(have.text(profile))
        self.categories_title.should(have.text(categories))

    def should_categories_name(self, name_category):
        self.categories_name(name_category).should(be.visible)

    def should_elements_present_in_page(self):
        self.user_name.should(be.visible)
        self.name.should(be.visible)
        self.profile_button.should(be.visible)
        self.search_category.should(be.visible)
        self.image_profile.should(be.visible)

    def should_categories_update(self, categories_update):
        browser.driver.refresh()
        self.menu_categories.should(have.text(categories_update["name"]))


app_profile_page = ProfilePage()
