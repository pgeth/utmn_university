#1. HTTP и requests. Простой сервер средствами стандартной библиотеки. Рекомендуется после данного упражнения начать тренироваться на фреймворке FastApi.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

USERS = {}
ORDERS = []
NEXT_USER_ID = 1
NEXT_ORDER_ID = 1


class SimpleRESTHandler(BaseHTTPRequestHandler):

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length) if length > 0 else b""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except:
            return None

    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _error(self, status, msg):
        self._send_json({"error": msg}, status=status)

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/users":
            self.create_user()
        elif parsed.path == "/orders":
            self.create_order()
        else:
            self._error(404, "Not found")

    def do_GET(self):
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if parsed.path == "/orders":
            self.list_orders()
        elif parsed.path == "/orders/count":
            self.orders_count()
        elif len(parts) == 2 and parts[0] == "orders":
            self.get_order(parts[1])
        else:
            self._error(404, "Not found")

    def create_user(self):
        global NEXT_USER_ID
        data = self._read_json_body()

        if not data or "name" not in data:
            return self._error(400, "Field 'name' is required")

        user = {"id": NEXT_USER_ID, "name": data["name"]}
        USERS[NEXT_USER_ID] = user
        NEXT_USER_ID += 1
        self._send_json(user, 201)

    def create_order(self):
        global NEXT_ORDER_ID
        data = self._read_json_body()

        required = ("user_id", "item", "amount")
        if not data or not all(k in data for k in required):
            return self._error(400, "Fields 'user_id', 'item', 'amount' required")

        user_id = data["user_id"]
        if user_id not in USERS:
            return self._error(400, "User does not exist")

        try:
            amount = int(data["amount"])
        except:
            return self._error(400, "'amount' must be integer")

        order = {
            "id": NEXT_ORDER_ID,
            "user_id": user_id,
            "item": data["item"],
            "amount": amount,
        }
        NEXT_ORDER_ID += 1
        ORDERS.append(order)

        self._send_json(order, 201)

    def list_orders(self):
        self._send_json(ORDERS)

    def orders_count(self):
        self._send_json({"count": len(ORDERS)})

    def get_order(self, oid):
        try:
            oid = int(oid)
        except:
            return self._error(400, "Order id must be integer")

        for order in ORDERS:
            if order["id"] == oid:
                return self._send_json(order)

        self._error(404, "Order not found")


def run(host="127.0.0.1", port=8000):
    print(f"Serving on http://{host}:{port}")
    server = HTTPServer((host, port), SimpleRESTHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.server_close()


if __name__ == "__main__":
    run()
