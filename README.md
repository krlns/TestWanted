<h1 align="center">
Test
</h1>

<hr>
<p>Для того, чтобы клонировать репозиторий, выполните команду:</p>

    git clone git@github.com:krlns/TestWanted.git
<hr>

<h3>Зайдите в папку куда склонировали репозиторий и выполните команды:</h3>
<ul><li>

    docker-compose up --build
</li></ul>

<h1>Описание API:</h1>
<h3>Регистрация нового пользователя::</h3>
<ul><li>

    curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "password123"}'
</li></ul>
<h3>Аутентификация и получение JWT токена:</h3>
<ul><li>

    curl -X POST "http://localhost:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=password123"

</li></ul>
<h3>Получение информации о пользователе по email:</h3>
<ul><li>

    curl -X GET "http://localhost:8000/auth/users/test@example.com"
</li></ul>
<h3>Смена пароля:</h3>
<ul><li>

    curl -X POST "http://localhost:8000/auth/change-password?new_password=newpassword123" -H "Authorization: Bearer <your_jwt_token>"
</li></ul>
<h3>Начисление баланса пользователю:</h3>
<ul><li>

    curl -X PATCH "http://localhost:8000/auth/users/1/balance?amount=<amount>" -H "Authorization: Bearer <your_jwt_token>"
</li></ul>
<h3>Перевод средств между пользователями:</h3>
<ul><li>

    curl -X POST "http://localhost:8001/transactions/transfer" -H "Authorization: Bearer <your_jwt_token>" -H "Content-Type: application/json" -d '{"receiver_email": "receiver@example.com", "amount": 100.0}'

</li></ul>
<h3>Получение истории транзакций:</h3>
<ul><li>

    curl -X GET "http://localhost:8001/transactions/transactions" -H "Authorization: Bearer <your_jwt_token>"
</li></ul>