import grpc

from performance_tests.contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from performance_tests.contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from performance_tests.contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from performance_tests.contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from performance_tests.contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest, OpenDebitCardAccountResponse
from performance_tests.contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import MakeTopUpOperationRequest, MakeTopUpOperationResponse
from performance_tests.contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import GetOperationReceiptRequest, GetOperationReceiptResponse
from performance_tests.tools.fakers import fake  # Используем генератор фейковых данных, созданный ранее
from performance_tests.contracts.services.operations.operation_pb2 import OperationStatus

# Устанавливаем соединение с gRPC-сервером по адресу localhost:9003
channel = grpc.insecure_channel("localhost:9003")

# Создаём gRPC-клиент для UsersGatewayService
users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service_stub = AccountsGatewayServiceStub(channel)
operations_gateway_service_stub = OperationsGatewayServiceStub(channel)

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
open_debit_card_account_response: OpenDebitCardAccountResponse = accounts_gateway_service_stub.OpenDebitCardAccount(
    open_debit_card_account_request
)
print('Open debit card account response:', open_debit_card_account_response)

make_top_up_operation_request = MakeTopUpOperationRequest(
    status=OperationStatus.OPERATION_STATUS_COMPLETED,
    amount=fake.amount(),
    card_id=open_debit_card_account_response.account.cards[0].id,
    account_id=open_debit_card_account_response.account.id
)
make_top_up_operation_response: MakeTopUpOperationResponse = operations_gateway_service_stub.MakeTopUpOperation(
    make_top_up_operation_request
)
print('Make top up operation response:', make_top_up_operation_response)

get_operation_receipt_request = GetOperationReceiptRequest(operation_id=make_top_up_operation_response.operation.id)
get_operation_receipt_response: GetOperationReceiptResponse = operations_gateway_service_stub.GetOperationReceipt(
    get_operation_receipt_request
)
print('Get operation receipt response:', get_operation_receipt_response)
