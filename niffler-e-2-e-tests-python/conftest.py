import os

import pytest
from dotenv import load_dotenv
from selene import browser, be
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDB
from databases.user_db import UsersDB
from models.config import Envs
from models.spend import SpendRequestModel, CategoryRequest
from pages.auth_page import auth_page
from pages.spend_page import app_spend_page
from faker import Faker


@pytest.fixture(scope='session')
def envs() -> Envs:
    load_dotenv()
    return Envs(
        profile_url=os.getenv('PROFILE_URL'),
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        registration_url=os.getenv("REGISTRATION_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        auth_db_url=os.getenv("AUTH_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )


@pytest.fixture(scope='session')
def auth(envs):
    auth_page.aurh_form(
        url=envs.frontend_url,
        username=envs.test_username,
        password=envs.test_password
    )
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope='session')
def spend_bd(envs) -> SpendDB:
    return SpendDB(envs.spend_db_url)


@pytest.fixture(scope='session')
def auth_bd(envs) -> UsersDB:
    return UsersDB(envs.auth_db_url)


@pytest.fixture(scope='session')
def delete_user_from_bd(request, auth_bd):
    yield
    auth_bd.delete_user_from_database()


@pytest.fixture(params=[])
def category(request, spends_client, spend_bd):
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category
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
def profile_page(auth, envs):
    browser.open(envs.profile_url)


@pytest.fixture()
def delete_after_create_spend(request, auth, envs):
    name_category = request.param  # Получаем имя категории из параметров
    yield
    # Выполняем удаление траты после теста
    app_spend_page.delete_spend(name_category)


@pytest.fixture
def spends_update(request, spends_client, spends):
    # Получаем данные для обновления из параметров
    update_data = request.param

    # Выполняем обновление траты
    response = spends_client.update_spends(
        SpendRequestModel(
            id=spends.id,
            amount=update_data.get("amount", spends.amount),
            description=update_data.get("description", spends.description),
            category=CategoryRequest(name=spends.category.name).model_dump(),
            currency=update_data.get("currency", spends.currency)
        ).model_dump()
    )

    yield response


@pytest.fixture()
def categories_update(category, spends_client):
    faker = Faker()
    response = spends_client.update_categories(
        {"name": faker.text(10),
         "id": category.id
         }
    )
    yield response
    try:
        spends_client.update_categories(
            {"id": category.id,
             "archived": True,
             "name": response["name"]
             }
        )
    except Exception:
        pass
