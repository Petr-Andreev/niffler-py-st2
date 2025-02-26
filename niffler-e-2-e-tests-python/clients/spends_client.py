from urllib.parse import urljoin

import requests

from models.spend import CategoriesModel, SpendsModel


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def get_categories(self) -> list[CategoriesModel]:
        response = self.session.get(urljoin(self.base_url, '/api/categories/all'))
        response.raise_for_status()
        return [CategoriesModel.model_validate(item) for item in response.json()]

    def add_category(self, name: str) -> CategoriesModel:
        response = self.session.post(urljoin(self.base_url, '/api/categories/add'), json={
            'name': name
        })
        response.raise_for_status()
        return CategoriesModel.model_validate(response.json())

    def get_spends(self) -> list[SpendsModel]:
        url = urljoin(self.base_url, '/api/spends/all')
        response = self.session.get(url)
        response.raise_for_status()
        return [SpendsModel.model_validate(item) for item in response.json()]

    def add_spends(self, body) -> SpendsModel:
        url = urljoin(self.base_url, '/api/spends/add')
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return SpendsModel.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        url = urljoin(self.base_url, '/api/spends/remove')
        response = self.session.delete(url, params={'ids': ids})
        response.raise_for_status()

    def update_spends(self, body: dict):
        url = urljoin(self.base_url, '/api/spends/edit')
        response = self.session.patch(url, json=body)
        response.raise_for_status()
        return response

    def update_categories(self, body: dict):
        url = urljoin(self.base_url, '/api/categories/update')
        response = self.session.patch(url, json=body)
        response.raise_for_status()
        return response.json()
