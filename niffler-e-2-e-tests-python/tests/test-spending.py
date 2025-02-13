from selene import browser, be, have
import requests


def test_successful_registration():
    browser.open('http://auth.niffler.dc:9000/login')
    browser.element('.form__register').click()
    browser.element('input[name=username]').set_value('katya')
    browser.element('input[name=password]').set_value('12345')
    browser.element('input[name=passwordSubmit]').set_value('12345')
    browser.element('button[type=submit]').click()
    browser.element('.form__paragraph').should(have.text("Congratulations! You've registered!"))
    browser.element('.form_sign-in').should(be.visible).should(be.clickable)


# Тесты на авторизацию
# 1. Пустой логин + пароль
def test_unsuccessful_authorization_empty_login():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()


# 2. Пустой пароль + логин
def test_unsuccessful_authorization_empty_password():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()


# 3. Пустой логин + пустой пароль
def test_unsuccessful_authorization_empty_login_and_empty_password():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('')
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()


def test_should_have_title_spending():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
    browser.element('button[type=submit]').click()
    browser.element('#spendings > h2').should(have.text('History of Spendings'))


def test_spending_should_be_created():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
    browser.element('button[type=submit]').click()
    browser.element('//a[.="New spending"]').click()
    browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3').should(have.text('Add new spending'))
    browser.element('#amount').set_value('100500')
    browser.element('#category').set_value('Test-category')
    browser.element('#description').set_value('Test-create-category')
    browser.element('#save').click()
    browser.element('//span[.="Test-create-category"]').should(be.visible).should(be.clickable)


# Добавление траты с нулевым прайсом
def test_spending_should_be_created_empty_price():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
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
def test_spending_should_be_created_empty_categories():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
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
def test_spending_should_be_created_dollar_price():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
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
def test_spending_should_be_created_euro_price():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
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
def test_spending_should_be_created_specific_date_on_calendar():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
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


def test_spending_should_be_deleted():
    url = "http://gateway.niffler.dc:8090/api/spends/add"

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer eyJraWQiOiI4YjUwNGMxZS1lNGQ5LTRiZWYtOGRkMi0wYjM3MDVjYjk0YzgiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJwZXR5YSIsImF1ZCI6ImNsaWVudCIsImF6cCI6ImNsaWVudCIsImF1dGhfdGltZSI6MTczOTQzMjg5MSwiaXNzIjoiaHR0cDovL2F1dGgubmlmZmxlci5kYzo5MDAwIiwiZXhwIjoxNzM5NDM0NjkxLCJpYXQiOjE3Mzk0MzI4OTEsImp0aSI6IjU1YTFkMzA3LTY2M2MtNDg1ZC1iOGYwLWU1M2MwMjg5ZWEyYSIsInNpZCI6IlYtSExBSnA2ZVlkUVFnNktnS1FYLVptWUQ1MWZ0T0l3Y0lobGpHOUxvOEkifQ.Jyrr69jSt9IFmjACiuDJ5Lu98J-DHwe7srzIx7Lj6viyl4gh4xpKXuCv3InB5TIGwF4l6nRiytCQEkT_3vJuqm5peQSw8U97mHYpvYKpz-aJEZL-t2h8zqamHoTGKAR7MGa-4T6kLZWJAkgztlbbQd6DhmUqCapS8bh_StJHQM9ntY71lOnqZSt2vrpVa9q9uNXglgdeEPDq1AdVAleBmFcGvQOnW3Z57n051_wy71-sVcsphDlmT65vOGUlDjEL_XAce_wXhBBTUx18wjuBuUmK3y0k6iUtVrNvJOjFJy0IWR3tLVthNxcElOj719PHlEAMst_e10Advmrh118EfQ",
        "Content-Type": "application/json",
        "Origin": "http://frontend.niffler.dc",
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

    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value('petya')
    browser.element('input[name=password]').set_value('12345')
    browser.element('button[type=submit]').click()
    browser.element('//span[.="Test_for_deleted"]').should(be.visible).click()
    browser.element('#delete').click()
    browser.all('//button[.="Delete"]').second.click()
    browser.element('//span[.="Test_for_deleted"]').should(be.hidden)
    browser.element('//p[.="There are no spendings"]').should(be.visible)
