from pages.auth_page import registration_page, auth_page


# @pytest.mark.skip('Надо добавить удаление аккаунта после завершения теста')
def test_successful_registration(envs):
    registration_page.registration_form(
        url=f"{envs.registration_url}/login",
        username=envs.test_username,
        password=envs.test_password,
        congratulations_text="Congratulations! You've registered!"
    )


# Тесты на авторизацию
# 1. Пустой логин + пароль
def test_unsuccessful_authorization_empty_login(envs):
    auth_page.aurh_form(
        url=envs.frontend_url,
        username='',
        password=envs.test_password
    )


# 2. Пустой пароль + логин
def test_unsuccessful_authorization_empty_password(envs):
    auth_page.aurh_form(
        url=envs.frontend_url,
        username=envs.test_username,
        password=''
    )


# 3. Пустой логин + пустой пароль
def test_unsuccessful_authorization_empty_login_and_empty_password(envs):
    auth_page.aurh_form(
        url=envs.frontend_url,
        username='',
        password=''
    )
