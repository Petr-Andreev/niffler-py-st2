from selene import browser, be, have


# @pytest.mark.skip('Надо добавить удаление аккаунта после завершения теста')
def test_successful_registration(envs):
    browser.open(f"{envs.registration_url}/login")
    browser.element('.form__register').click()
    browser.element('input[name=username]').set_value(envs.test_username)
    browser.element('input[name=password]').set_value(envs.test_password)
    browser.element('input[name=passwordSubmit]').set_value(envs.test_password)
    browser.element('button[type=submit]').click()
    browser.element('.form__paragraph').should(have.text("Congratulations! You've registered!"))
    browser.element('.form_sign-in').should(be.visible).should(be.clickable)


# Тесты на авторизацию
# 1. Пустой логин + пароль
def test_unsuccessful_authorization_empty_login(envs, app_user):
    username, password = app_user
    browser.open(envs.frontend_url)
    browser.element('input[name=username]').set_value('')
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()


# 2. Пустой пароль + логин
def test_unsuccessful_authorization_empty_password(envs, app_user):
    username, password = app_user
    browser.open(envs.frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()


# 3. Пустой логин + пустой пароль
def test_unsuccessful_authorization_empty_login_and_empty_password(envs):
    browser.open(envs.frontend_url)
    browser.element('input[name=username]').set_value('')
    browser.element('input[name=password]').set_value('')
    browser.element('button[type=submit]').click()
