import time
import httpx

# Создание нового пользователя
create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}
create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

# Открытие кредитный счёта
open_credit_card_account_payload = {
    "userId": create_user_response_data["user"]["id"]
}
open_credit_card_account_response = httpx.post(
    "http://localhost:8003/api/v1/accounts/open-credit-card-account",
    json=open_credit_card_account_payload
)
open_credit_card_account_response_data = open_credit_card_account_response.json()

# Выполнение операции пополнения счёта
make_purchase_operation_payload = {
    "status": "IN_PROGRESS",
    "amount": 77.99,
    "category": "taxi",
    "cardId": open_credit_card_account_response_data["account"]["cards"][0]["id"],
    "accountId": open_credit_card_account_response_data["account"]["id"]
}
purchase_operation_response = httpx.post(
    "http://localhost:8003/api/v1/operations/make-purchase-operation",
    json=make_purchase_operation_payload
)
operation_id = purchase_operation_response.json()['operation']['id']
operation_receipt = httpx.get(f"http://localhost:8003/api/v1/operations/operation-receipt/{operation_id}")
print('operation_receipt:', operation_receipt.json())