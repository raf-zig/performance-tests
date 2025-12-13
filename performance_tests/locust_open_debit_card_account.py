from locust import HttpUser, between, task

from tools.fakers import fake  # генератор случайных данных


class OpenDebitCardAccountScenarioUser(HttpUser):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)

    # В этой переменной будем хранить id пользователя
    user_id: str

    def on_start(self) -> None:
        request = {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }
        response = self.client.post("http://localhost:8003/api/v1/users", json=request)

        # Сохраняем полученный id
        self.user_id = response.json()["user"]["id"]

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: получение информации о пользователе.
        Здесь мы выполняем POST-запрос к api/v1/accounts/open-debit-card-account{self.user_id}.
        """
        self.client.post(
            f"http://localhost:8003/api/v1/accounts/open-debit-card-account{self.user_id}",
            name="api/v1/accounts/open-debit-card-account{self.user_id}"  # Явное указание имени группы запросов
        )
