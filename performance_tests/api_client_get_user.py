from performance_tests.clients.http.gateway.users.client import build_users_gateway_http_client

# Инициализируем клиент UsersGatewayHTTPClient
users_gateway_client = build_users_gateway_http_client()

# Отправляем POST запрос на создание пользователя
create_user_response = users_gateway_client.create_user()
print('Create user data:', create_user_response)

# Отправляем GET запрос на получение данных пользователя
get_user_response = users_gateway_client.get_user(create_user_response.user.id)
print('Get user data:', get_user_response)
