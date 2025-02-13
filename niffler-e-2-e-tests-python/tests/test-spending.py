import pytest
from selene import browser, be, have
import requests
from conftest import Pages


def test_successful_registration(registration_url, app_user):
    username, password = app_user
    browser.open(f"{registration_url}/login")
    browser.element('.form__register').click()
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('input[name=passwordSubmit]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('.form__paragraph').should(have.text("Congratulations! You've registered!"))
    browser.element('.form_sign-in').should(be.visible).should(be.clickable)


# Тесты на авторизацию
# 1. Пустой логин + пароль
def test_unsuccessful_authorization_empty_login(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value('')
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()


# 2. Пустой пароль + логин
def test_unsuccessful_authorization_empty_password(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()


# 3. Пустой логин + пустой пароль
def test_unsuccessful_authorization_empty_login_and_empty_password(frontend_url):
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value('')
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()


@Pages.main_page
def test_should_have_title_spending():
    browser.element('#spendings > h2').should(have.text('History of Spendings'))


def test_spending_should_be_created(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


# Добавление траты с нулевым прайсом
def test_spending_should_be_created_empty_price(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('')
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('.input__helper-text').should(be.visible).should(
        have.text('Amount has to be not less then 0.01')
    )


# Добавление траты без указания категории
def test_spending_should_be_created_empty_categories(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100')
    browser.element('#category').set_value('')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('.input__helper-text').should(be.visible).should(
        have.text('Please choose category')
    )


# Добавление траты с долларовым прайсом
def test_spending_should_be_created_dollar_price(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#currency').click()
    browser.element('//span[.="USD"]').click()
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


# Добавление траты с евро прайсом
def test_spending_should_be_created_euro_price(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#currency').click()
    browser.element('//span[.="EUR"]').click()
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


# Добавление траты на указанную дату в календаре
def test_spending_should_be_created_specific_date_on_calendar(frontend_url, app_user):
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
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
    browser.element('//span[.="Test-create-category"]').should(be.visible)


@Pages.main_page
@pytest.mark.parametrize("category", ['test'], indirect=True)
def test_spending_should_be_deleted(frontend_url, gateway_url, app_user, category):

    assert False
    url = f"{gateway_url}/api/spends/add"

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "amount": "100500",
        "description": "Test_for_deleted",
        "currency": "RUB",
        "spendDate": "2025-02-12T15:39:41.194Z",
        "category": {
            "name": "Test-category"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    # Проверяем статус ответа
    assert response.status_code == 201

    browser.open(frontend_url)
    browser.element('//span[.="Test_for_deleted"]').should(be.visible).click()
    browser.element('#delete').click()
    browser.all('//button[.="Delete"]').second.click()
    browser.element('//span[.="Test_for_deleted"]').should(be.hidden)
    browser.element('//p[.="There are no spendings"]').should(be.visible)
