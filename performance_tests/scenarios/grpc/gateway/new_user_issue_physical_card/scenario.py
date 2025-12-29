from locust import task

from performance_tests.clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from performance_tests.contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountResponse
from performance_tests.contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import IssuePhysicalCardResponse
from performance_tests.contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from performance_tests.tools.locust.user import LocustBaseUser


# Класс сценария: описывает последовательный флоу нового пользователя
class IssuePhysicalCardScenarioUserTaskSet(GatewayGRPCSequentialTaskSet):
    # Храним ответы от предыдущих шагов, чтобы использовать их в следующих задачах
    create_user_response: CreateUserResponse | None = None
    issue_physical_card_response: IssuePhysicalCardResponse | None = None
    open_open_debit_card_account_response: OpenDebitCardAccountResponse | None = None

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
        # Невозможно Выпуск физической карты без open_debit_card_account
        if not self.open_debit_card_account:
            return

        # Выпуск физической карты
        self.issue_physical_card_response = self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_open_debit_card_account_response.account.id
        )

class IssuePhysicalCardScenarioUser(LocustBaseUser):
    # Назначаем сценарий, который будет выполняться этим пользователем
    tasks = [IssuePhysicalCardScenarioUserTaskSet]