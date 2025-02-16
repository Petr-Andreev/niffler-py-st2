import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    delete_after_create_spend = pytest.mark.usefixtures("delete_after_create_spend")


class TestData:
    category = lambda x: pytest.mark.parametrize('category', [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize('spends', [x],
                                               indirect=True,
                                               ids=lambda param: param['description'])
