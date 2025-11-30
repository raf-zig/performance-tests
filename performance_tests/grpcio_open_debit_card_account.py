import grpc

from performance_tests.contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from performance_tests.contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from performance_tests.contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from performance_tests.contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from performance_tests.contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest, OpenDebitCardAccountResponse
from performance_tests.tools.fakers import fake  # Используем генератор фейковых данных, созданный ранее

# Устанавливаем соединение с gRPC-сервером по адресу localhost:9003
channel = grpc.insecure_channel("localhost:9003")

# Создаём gRPC-клиент для UsersGatewayService
users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service_stub = AccountsGatewayServiceStub(channel)
# Формируем запрос на создание пользователя с рандомными данными
create_user_request = CreateUserRequest(
    email=fake.email(),
    last_name=fake.last_name(),
    first_name=fake.first_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)

create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)
print('Create user response:', create_user_response)

open_debit_card_account_request = OpenDebitCardAccountRequest(user_id=create_user_response.user.id)
open_debit_card_account_response: OpenDebitCardAccountResponse = accounts_gateway_service_stub.OpenDebitCardAccount(open_debit_card_account_request)
print('Open debit card account response:', open_debit_card_account_response)
