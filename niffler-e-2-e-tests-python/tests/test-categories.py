from marks import Pages, TestData
from pages.profile_page import app_profile_page
from faker import Faker

fake = Faker()
TEST_CATEGORY = fake.word()
CATEGORY_UPDATE = fake.word()


@Pages.profile_page
def test_title_in_page():
    app_profile_page.title_form(
        profile='Profile',
        categories='Categories'
    )


@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_add_categories(category):
    app_profile_page.should_categories_name(
        name_category=TEST_CATEGORY
    )


@Pages.profile_page
def test_elements_present_in_page():
    app_profile_page.should_elements_present_in_page()


@Pages.profile_page
@TestData.category(CATEGORY_UPDATE)
def test_update_categories(category, categories_update):
    app_profile_page.should_categories_update(
        categories_update=categories_update
    )
