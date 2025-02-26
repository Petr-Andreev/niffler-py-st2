import pytest


class Pages:
    profile_page = pytest.mark.usefixtures("profile_page")
    main_page = pytest.mark.usefixtures("main_page")
    delete_after_create_spend = lambda name_category: pytest.mark.parametrize(
        "delete_after_create_spend", [name_category], indirect=True
    )


class TestData:
    category = lambda x: pytest.mark.parametrize('category', [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize('spends', [x],
                                               indirect=True,
                                               ids=lambda param: param)
    spends_update = lambda update_data: pytest.mark.parametrize(
        "spends_update",  # Имя фикстуры
        [update_data],  # Список с данными для обновления
        indirect=True,  # Параметры передаются в фикстуру
        ids=lambda param: f"spends_update_{param.get('description', 'unknown')}"  # Генерация ID для теста
    )
