from typing import TypedDict

from httpx import Response
from performance_tests.clients.http.gateway.client import build_gateway_http_client
from performance_tests.clients.http.client import HTTPClient


class CardDict(TypedDict):
    """
    Описание структуры карты.
    """
    id: str
    pin: str
    cvv: str
    type: str
    status: str
    accountId: str
    cardNumber: str
    cardHolder: str
    expiryDate: str
    paymentSystem: str

class IssueVirtualCardRequestDict(TypedDict):
    """
    Структура данных для создания виртуальной карты пользователя.
    """
    userId: str
    accountId: str

class IssueVirtualCardResponseDict(TypedDict):
    """
    Описание структуры ответа выпуска виртуальной карты.
    """
    card: CardDict

class IssuePhysicalCardRequestDict(TypedDict):
    """
    Структура данных для создания физической карты пользователя.
    """
    userId: str
    accountId: str

class IssuePhysicalCardResponseDict(TypedDict):
    """
    Описание структуры ответа выпуска физической карты.
    """
    card: CardDict

class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с api/v1/cards сервиса http-gateway.
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestDict) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param request: Словарь с данными виртуальной карты пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(f"/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        """
        Создание нового пользователя.

        :param request: Словарь с данными физической карты пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/cards/issue-physical-card", json=request)

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseDict:
        request = IssueVirtualCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_virtual_card_api(request)
        return response.json()

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseDict:
        request = IssuePhysicalCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_physical_card_api(request)
        return response.json()

def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())
