from datetime import date

from pydantic import BaseModel, Field


# Добавили модель CardSchema
class CardSchema(BaseModel):
    id: str
    pin: str
    cvv: str
    type: str
    status: str
    account_id: str = Field(alias="accountId")  # Используем alias
    card_number: str = Field(alias="cardNumber")  # Используем alias
    card_holder: str = Field(alias="cardHolder")  # Используем alias
    expiry_date: date = Field(alias="expiryDate")  # Используем alias
    payment_system: str = Field(alias="paymentSystem")  # Используем alias


class AccountSchema(BaseModel):
    id: str
    type: str
    # Вложенный объект для списка карт привязанных к счету
    cards: list[CardSchema]
    status: str
    balance: float

# Инициализируем модель AccountSchema через JSON
account_json = """
{
    "id": "account-id",
    "type": "CREDIT_CARD",
    "status": "ACTIVE",
    "balance": 777.11
}
"""
account_json_model = AccountSchema.model_validate_json(account_json)
print('Account JSON model:', account_json_model)
