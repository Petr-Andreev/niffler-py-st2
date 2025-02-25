import time
from selene import browser, have, be
from marks import Pages, TestData

TEST_CATEGORY = "investments"


@Pages.main_page
def test_title_in_page():
    time.sleep(5)
    browser.element('[class="MuiTypography-root MuiTypography-h5 css-w1t7b3"]').should(
        have.text('Profile'))
    browser.element('[class ="MuiTypography-root MuiTypography-h5 css-1pam1gy"]').should(
        have.text('Categories'))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
def test_add_categories(category):
    browser.element('[class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-3w20vr"]').should(
        have.text("investments"))


@Pages.main_page
def test_elements_present_in_page():
    browser.element('#username').should(be.visible)
    browser.element('#name').should(be.visible)
    browser.element('[class="MuiTouchRipple-root css-w0pj6f"]').should(be.visible)
    browser.element('#category').should(be.visible)
    browser.element('.image__input-label').should(be.visible)
