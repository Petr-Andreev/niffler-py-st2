from pydantic import BaseModel, Field, StrictFloat
from datetime import datetime, timezone
from typing import Literal


# Модель для категории
class CategoriesModel(BaseModel):
    id: str | None
    name: str
    username: str | None = None
    archived: bool | None = None


# Модель для траты
class SpendsModel(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    currency: str
    spendDate: str = Field(alias="spendDate")  # Используем alias для соответствия JSON
    category: CategoriesModel  # Вложенная модель для категории


class SpendResponseModel(BaseModel):
    id: str
    spendDate: str
    category: CategoriesModel
    currency: Literal["RUB", "EUR", "USD", "KZT"]
    amount: StrictFloat
    description: str
    username: str


class CategoryRequest(BaseModel):
    id: str | None = None
    name: str
    username: str | None = None
    archived: bool | None = None


class SpendRequestModel(BaseModel):
    id: str | None = None
    spendDate: str = Field(default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z")
    category: CategoryRequest
    currency: Literal["RUB", "EUR", "USD", "KZT"]
    amount: float
    description: str
    username: str | None = None
