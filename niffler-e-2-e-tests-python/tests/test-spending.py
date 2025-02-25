import pytest
from selene import browser, be, have
from marks import Pages, TestData

TEST_CATEGORY = "car4"


@Pages.main_page
def test_spending_title_exist():
    browser.element('#spendings > h2').should(have.text('History of Spendings'))


@Pages.main_page
@Pages.delete_after_create_spend
def test_created_spend():
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


@Pages.main_page
# Добавление траты с нулевым прайсом
def test_spending_should_be_created_empty_price():
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('')
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('.input__helper-text').should(be.visible).should(
        have.text('Amount has to be not less then 0.01')
    )


@Pages.main_page
# Добавление траты без указания категории
def test_spending_should_be_created_empty_categories():
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100')
    browser.element('#category').set_value('')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('.input__helper-text').should(be.visible).should(
        have.text('Please choose category')
    )


@Pages.main_page
@Pages.delete_after_create_spend
# Добавление траты с долларовым прайсом
def test_spending_should_be_created_dollar_price():
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#currency').click()
    browser.element('//span[.="USD"]').click()
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


@Pages.main_page
@Pages.delete_after_create_spend
# Добавление траты с евро прайсом
def test_spending_should_be_created_euro_price():
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#currency').click()
    browser.element('//span[.="EUR"]').click()
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


@Pages.main_page
@Pages.delete_after_create_spend
# Добавление траты на указанную дату в календаре
def test_spending_should_be_created_specific_date_on_calendar():
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#category').set_value('Test-category')
    browser.element('.css-15btvqp').click()
    browser.element('.MuiPickersCalendarHeader-label.css-1v994a0').click()
    browser.element('//button[.="2024"]').click()
    browser.element('//button[.="10"]').click()
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    {
        "amount": "100500",
        "description": "Test_for_deleted",
        "currency": "RUB",
        "spendDate": "2025-02-12T15:39:41.194Z",
        "category": {
            "name": TEST_CATEGORY
        }
    }
)
def test_spending_should_be_deleted(category, spends):
    # Проверяем наличие траты
    browser.element(f'//span[.="Test_for_deleted"]').should(be.visible).click()
    # Удаляем трату
    browser.element('#delete').click()
    browser.all('//button[.="Delete"]').second.click()
    # Проверяем, что траты больше нет
    browser.element(f'//span[.="Test_for_deleted"]').should(be.hidden)
    # Проверяем сообщение о пустом списке трат
    browser.element('//p[.="There are no spendings"]').should(be.visible)


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends_list(

    [
        {
            "amount": "11111",
            "description": "Test_currency",
            "currency": "RUB",
            "spendDate": "2025-02-12T15:39:41.194Z",
            "category": {
                "name": TEST_CATEGORY
            }
        },
        {
            "amount": "22222",
            "description": "Test_currency_rub2",
            "currency": "RUB",
            "spendDate": "2025-02-13T15:39:41.194Z",
            "category": {
                "name": TEST_CATEGORY
            }
        },
        {
            "amount": "33333",
            "description": "Test_currency_eur",
            "currency": "EUR",
            "spendDate": "2025-02-14T15:39:41.194Z",
            "category": {
                "name": TEST_CATEGORY
            }
        }
    ]

)
def test_spending_should_be_deleted(category, spends_list):
    # Проверяем наличие всех созданных трат
    browser.element(f'//span[.="Test_currency"]').should(be.visible).click()






# 2) Добавить несколько трат с разными названиями, проверить, что работают поиск по названию
# 3) Загрузить фото в профиль, проверить что она загрузилась
# 4) добавить имя в профиль, проверить, что оно сохранилось
# 5) добавление категории вручную - нажатие ентер и проверка что категория добавилась
# 6) изменить название категории
# 7) добавить категорию в архив, проверка что она добавилась в архив (сдвинуть слайдер₽
# 8) убрать из архива
# 9) проверка логаута
