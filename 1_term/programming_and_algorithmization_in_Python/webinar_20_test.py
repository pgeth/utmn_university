import pytest
import requests
import threading
import time
from http.server import HTTPServer
import webinar_20


@pytest.fixture(scope="session")
def server():
    host = "127.0.0.1"
    port = 8888 

    httpd = HTTPServer((host, port), webinar_20.SimpleRESTHandler)

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    time.sleep(0.5)

    try:
        yield host, port
    finally:
      httpd.shutdown()
      httpd.server_close()


@pytest.fixture(autouse=True)
def reset_data():
    webinar_20.USERS.clear()
    webinar_20.ORDERS.clear()
    webinar_20.NEXT_USER_ID = 1
    webinar_20.NEXT_ORDER_ID = 1
    yield


@pytest.fixture
def created_user(server):
    response = requests.post(
        f"{server}/users",
        json={"name": "Test User"}
    )
    return response.json()


class TestUsers:
    """Примеры тестов для работы с пользователями"""

    def test_create_user_success(self, server):
        """Пример успешного создания пользователя"""
        response = requests.post(
            f"{server}/users",
            json={"name": "John Doe"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"

    def test_create_user_without_name(self, server):
        """Пример теста валидации - создание пользователя без имени"""
        response = requests.post(
            f"{server}/users",
            json={}
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"] == "Field 'name' is required"


class TestOrders:
    """Примеры тестов для работы с заказами"""

    def test_create_order_success(self, server, created_user):
        """Пример успешного создания заказа"""
        response = requests.post(
            f"{server}/orders",
            json={
                "user_id": created_user["id"],
                "item": "Laptop",
                "amount": 2
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["user_id"] == created_user["id"]
        assert data["item"] == "Laptop"
        assert data["amount"] == 2

    def test_get_order_not_found(self, server):
        """Пример теста обработки ошибок - получение несуществующего заказа"""
        response = requests.get(f"{server}/orders/999")

        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "Order not found"
