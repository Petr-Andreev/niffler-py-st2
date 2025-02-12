from selene import browser, be, have
import requests

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


def test_spending_should_be_deleted():
    url = "http://gateway.niffler.dc:8090/api/spends/add"

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer eyJraWQiOiJjNTM2YzYyYi03YWFkLTRkMDktYjRlMy1kOGY1MDFhMmVmNjIiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJwZXR5YSIsImF1ZCI6ImNsaWVudCIsImF6cCI6ImNsaWVudCIsImF1dGhfdGltZSI6MTczOTM3NDQ3MiwiaXNzIjoiaHR0cDovL2F1dGgubmlmZmxlci5kYzo5MDAwIiwiZXhwIjoxNzM5Mzc2MjcyLCJpYXQiOjE3MzkzNzQ0NzIsImp0aSI6IjMyMTdlMjg5LWFiOGQtNGM3MC1iZjJiLTIwMmQ1M2U0ZTUyYSIsInNpZCI6IjVwTDg5djhvcUNkdjF3SkFRREMwMll2MDFBX3Bsb0tIYjJ1NkNjSFc4T1UifQ.mNjWMw3LV0Rk1xf-JvTK3PHagUPIq5IKDbYei5Wva1gF7BxidfxA02DwP6Gh-Cz6M9cFLDqX3yZhrqtobaol4ANLO0Q_0JW7mpBMbc2MeO75UH0Wp1fjvvJLIfU0cVEcrgiTgBEDMTiFUtvwikSCI9qBomxTmgHyJ2RsWkHiDK_umSgkeT-_5WHW5OZh496YGuZpZadpUFKSsKaNSpxNH-WROlnLFfNwWGoVhKKSd8dgxWMuhFd0Zm0dw6pNpIiyKJ-368Oih1gYzptCSrGhPL0Xrj6hJLLFNmG3gtWh5gRlzkjB8dvncE5ezLxVEnSOXg9HbBQT10e208gSeTV1Jg",
        "Content-Type": "application/json",
        "Origin": "http://frontend.niffler.dc",
    }

    data = {
        "amount": "0100500",
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

