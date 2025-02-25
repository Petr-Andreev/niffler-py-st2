import os

import pytest
from dotenv import load_dotenv
from selene import browser, be
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDB
from models.config import Envs


@pytest.fixture(scope='session')
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        registration_url=os.getenv("REGISTRATION_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )


@pytest.fixture(scope='session')
def auth(envs):
    browser.open(envs.frontend_url)
    browser.element('input[name=username]').set_value(envs.test_username)
    browser.element('input[name=password]').set_value(envs.test_password)
    browser.element('button[type=submit]').click()
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope='session')
def spend_bd(envs) -> SpendDB:
    return SpendDB(envs.spend_db_url)


@pytest.fixture(params=[])
def category(request, spends_client, spend_bd):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.name
    spend_bd.delete_user_categories(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture
def spends_list(request, spends_client):
    # Получаем список JSON-объектов из параметров
    spend_data_list = request.param

    created_spends = []
    for spend_data in spend_data_list:
        # Создаем каждую трату
        test_spend = spends_client.add_spends(spend_data)
        created_spends.append(test_spend)

    yield created_spends  # Возвращаем список созданных трат

    # Удаляем все созданные траты после завершения теста
    all_spends = spends_client.get_spends()
    ids_to_remove = [spend.id for spend in created_spends if spend.id in [s.id for s in all_spends]]
    if ids_to_remove:
        spends_client.remove_spends(ids_to_remove)


@pytest.fixture()
def main_page(auth, envs):
    browser.open(envs.frontend_url)


@pytest.fixture()
def delete_after_create_spend(auth, envs):
    yield
    browser.element('//span[.="Test-category"]').should(be.visible).click()
    browser.element('#delete').click()
    browser.all('//button[.="Delete"]').second.click()
