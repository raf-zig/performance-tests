from locust import task

from performance_tests.clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from performance_tests.clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from performance_tests.clients.http.gateway.cards.schema import IssuePhysicalCardResponseSchema
from performance_tests.clients.http.gateway.users.schema import CreateUserResponseSchema
from performance_tests.tools.locust.user import LocustBaseUser


# Класс сценария: описывает последовательный флоу нового пользователя
class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    # Храним ответы от предыдущих шагов, чтобы использовать их в следующих задачах
    create_user_response: CreateUserResponseSchema | None = None
    issue_physical_card_response: IssuePhysicalCardResponseSchema | None = None
    open_open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None

    @task
    def create_user(self):
        # Первый шаг — создать нового пользователя
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        # Невозможно открыть счёт без созданного пользователя
        if not self.create_user_response:
            return

        # Открываем дебетовый счёт для нового пользователя
        self.open_open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def issue_physical_card(self):
        # Проверяем, что счёт успешно открыт
        if not self.open_open_debit_card_account_response:
            return

        # Выполняем issue_physical_card
        self.issue_physical_card_response = self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_open_debit_card_account_response.account.id
        )

class IssuePhysicalCardScenarioUser(LocustBaseUser):
    # Назначаем сценарий, который будет выполняться этим пользователем.
    tasks = [IssuePhysicalCardSequentialTaskSet]