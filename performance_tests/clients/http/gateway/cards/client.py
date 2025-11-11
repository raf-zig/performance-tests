from typing import TypedDict

from httpx import Response

from performance_tests.clients.http.client import HTTPClient


class CreateVirtualCardRequestDict(TypedDict):
    """
    Структура данных для создания виртуальной карты пользователя.
    """
    userId: str
    accountId: str

class CreatePhisicalCardRequestDict(TypedDict):
    """
    Структура данных для создания физической карты пользователя.
    """
    userId: str
    accountId: str

class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с api/v1/cards сервиса http-gateway.
    """

    def issue_virtual_card_api(self, request: CreateVirtualCardRequestDict) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param request: Словарь с данными виртуальной карты пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(f"/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: CreatePhisicalCardRequestDict) -> Response:
        """
        Создание нового пользователя.

        :param request: Словарь с данными физической карты пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/cards/issue-physical-card ", json=request)

