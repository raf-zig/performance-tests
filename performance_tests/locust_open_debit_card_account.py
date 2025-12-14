from locust import User, between, task

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client

class OpenDebitCardAccountScenarioUser(User):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)
    host = "localhost"
    users_gateway_client: UsersGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient

    def on_start(self) -> None:
        # Шаг 1: создаем API клиенты, встроенный в экосистему Locust (с хуками и поддержкой сбора метрик)
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)

        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)

        # Шаг 2: создаем пользователя через API
        self.create_user_response = self.users_gateway_client.create_user()


    @task
    def open_debit_card_account(self):
        self.create_accounts_response = self.accounts_gateway_client.open_debit_card_account(
            self.create_user_response.user.id
        )
