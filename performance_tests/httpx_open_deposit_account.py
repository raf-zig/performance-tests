import time

import httpx  # Импортируем библиотеку HTTPX

# Данные для создания пользователя
create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

# Выполняем запрос на создание пользователя
create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

user_id = {
  "userId": f"{create_user_response_data['user']['id']}"
}
open_deposit_account = httpx.post(
    "http://localhost:8003/api/v1/accounts/open-deposit-account", json=user_id
)
open_deposit_account_data = open_deposit_account.json()

# Выводим полученные данные
print("Open deposit account:", open_deposit_account_data)
print("Status Code:", open_deposit_account.status_code)


