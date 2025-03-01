import pytest
from selene import browser, have, be

from marks import Pages, TestData
from models.spend import SpendRequestModel, CategoryRequest
from pages.spend_page import app_spend_page
from faker import Faker

from resource import load_json_data

fake = Faker()
TEST_CATEGORY = fake.word()
NAME_CATEGORY = fake.word()
TEST_CATEGORY_FOR_ANY_SPEND = 'list_spends'


@Pages.main_page
def test_spending_title_exist():
    browser.element('#spendings > h2').should(have.text('History of Spendings'))


@Pages.main_page
@Pages.delete_after_create_spend(NAME_CATEGORY)
def test_created_spend(delete_after_create_spend):
    app_spend_page.create_spend(
        title='Add new spending',
        amount='100500',
        name_category=NAME_CATEGORY,
        description='Test-create-category',
    )


@Pages.main_page
# Добавление траты с нулевым прайсом
def test_spending_should_be_created_empty_price():
    app_spend_page.create_invalid_spand(
        title='Add new spending',
        amount='',
        name_category=NAME_CATEGORY,
        description='Test-create-category',
        text='Amount has to be not less then 0.01'
    )


@Pages.main_page
# Добавление траты без указания категории
def test_spending_should_be_created_empty_categories():
    app_spend_page.create_invalid_spand(
        title='Add new spending',
        amount='100',
        name_category='',
        description='Test-create-category',
        text='Please choose category'
    )


@Pages.main_page
@Pages.delete_after_create_spend(NAME_CATEGORY)
# Добавление траты с долларовым прайсом
def test_spending_should_be_created_dollar_price(delete_after_create_spend):
    app_spend_page.create_spend_different_currency(
        title='Add new spending',
        amount='100500',
        currency_val='USD',
        name_category=NAME_CATEGORY,
        description='Test-create-category'
    )


@Pages.main_page
@Pages.delete_after_create_spend(NAME_CATEGORY)
# Добавление траты с евро прайсом
def test_spending_should_be_created_euro_price(delete_after_create_spend):
    app_spend_page.create_spend_different_currency(
        title='Add new spending',
        amount='100500',
        currency_val='EUR',
        name_category=NAME_CATEGORY,
        description='Test-create-category'
    )


@pytest.mark.skip("This test not works")
@Pages.main_page
@Pages.delete_after_create_spend(NAME_CATEGORY)
# Добавление траты на указанную дату в календаре
def test_spending_should_be_created_specific_date_on_calendar(delete_after_create_spend):
    app_spend_page.create_spend_specific_date_on_calendar(
        title='Add new spending',
        amount='100500',
        name_category=NAME_CATEGORY,
        date='04/02/2023',
        value_date='Feb 04, 2023',
        description='Test-create-category'
    )


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendRequestModel(
        amount=100500,
        description='Test_for_deleted',
        category=CategoryRequest(**{'name': f'{TEST_CATEGORY}'}).model_dump(),
        currency="KZT"
    ).model_dump()
)
def test_delete_spending(category, spends):
    app_spend_page.verify_spend_delete(
        name_category=TEST_CATEGORY,
        title_text='There are no spendings'
    )


# Загружаем данные из spends.json
test_spends_data = load_json_data("spends.json")
@Pages.main_page
@TestData.category(TEST_CATEGORY_FOR_ANY_SPEND)
@pytest.mark.parametrize(
    "spends_list",  # Имя фикстуры
    [test_spends_data],  # Список данных для создания трат
    indirect=True  # Передаем параметры в фикстуру
)
def test_spending_different_currency(category, spends_list):
    # Проверяем наличие всех созданных трат
    browser.element(f'//span[.="{TEST_CATEGORY_FOR_ANY_SPEND}"]').should(be.visible).click()

    # Проверяем, что все description отображаются на странице
    app_spend_page.verify_description_create(
        [spend["description"] for spend in test_spends_data]
    )

@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendRequestModel(
        amount=108.51,
        description='QA-GURU Python ADVANCED 2',
        category=CategoryRequest(**{'name': f'{TEST_CATEGORY}'}).model_dump(),
        currency="RUB"
    ).model_dump()
)
@TestData.spends_update(
    SpendRequestModel(
        amount=200.51,
        description='Updated Spending Description',
        category=CategoryRequest(**{'name': f'{TEST_CATEGORY}'}).model_dump(),
        currency="EUR"
    ).model_dump()
)
def test_update_spending(category, spends, spends_update):
    # Проверяем, что данные были успешно обновлены
    app_spend_page.verify_spend_update(
        spends_update=spends_update
    )
