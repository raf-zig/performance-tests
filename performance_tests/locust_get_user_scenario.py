from locust import User, between, task

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.users.schema import CreateUserResponseSchema


class GetUserScenarioUser(User):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)
    host = "localhost"
    users_gateway_client: UsersGatewayHTTPClient
    create_user_response: CreateUserResponseSchema

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        # Шаг 1: создаем API клиент, встроенный в экосистему Locust (с хуками и поддержкой сбора метрик)
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)

        # Шаг 2: создаем пользователя через API
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def get_user(self):
        """
        Основная нагрузочная задача: получение информации о пользователе.
        Здесь мы выполняем GET-запрос к /api/v1/users/{user_id}.
        """
        self.users_gateway_client.get_user(self.create_user_response.user.id)
