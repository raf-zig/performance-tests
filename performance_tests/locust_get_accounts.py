from locust import User, between, task

# Импортируем схемы ответов, чтобы типизировать shared state
from performance_tests.clients.http.gateway.accounts.schema import OpenDepositAccountResponseSchema
from performance_tests.clients.http.gateway.locust import GatewayHTTPTaskSet
from performance_tests.clients.http.gateway.users.schema import CreateUserResponseSchema


class GetAccountsTaskSet(GatewayHTTPTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает сберегательный счёт.
    3. Получает документы по счёту (тариф и контракт).

    Использует базовый GatewayHTTPSequentialTaskSet и уже созданных в нём API клиентов.
    """
    # locust -f performance_tests/locust_get_accounts.py --headless --users 300 --spawn-rate 30 --run-time 3m --html .performance_tests/reports/locust_get_accounts_report.html
    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponseSchema | None = None
    open_deposit_account_response: OpenDepositAccountResponseSchema | None = None

    @task(2)
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """
        Открываем deposit счёт для созданного пользователя .
        Проверяем, что предыдущий шаг был успешным.
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, нет смысла продолжать

        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task(6)
    def get_accounts(self):
        """
        Получаем список всех счетов .
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, нет смысла продолжать

        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )


class GetAccountsScenarioUser(User):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения accounts.
    """
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 2)  # Имитируем паузы между выполнением сценариев
