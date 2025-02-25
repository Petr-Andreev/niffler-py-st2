from pydantic import BaseModel, Field


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
