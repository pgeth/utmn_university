# Возьмите за основу проект сервера загрузки файлов на Яндекс Диск. Для этого изучите вебинар «Интеграция с внешними сервисами на Python на примере Яндекс Диска».

# Вам нужно добавить в проект следующий функционал: при запросе HTML-страницы сервер должен проверять, какие файлы он уже загрузил, и заполнять фон HTML-элементам этих файлов цветом rgba(0, 200, 0, 0.25).

# Попробуйте самостоятельно найти в документации, как выставить элементу списка фоновый цвет. Самостоятельный поиск в документации — очень важный навык программирования. Но если информацию найти не получится, вы всегда можете задать вопрос преподавателю.

# Для получения информации о загруженных файлах используйте API-запрос.
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json


# Глобальная переменная для хранения OAuth токена
OAUTH_TOKEN = None


def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def get_uploaded_files(token):
    try:
        resp = get(
            "https://cloud-api.yandex.net/v1/disk/resources?path=Backup",
            headers={"Authorization": f"OAuth {token}"}
        )
        if resp.status_code == 200:
            data = json.loads(resp.text)
            if "_embedded" in data and "items" in data["_embedded"]:
                return [item["name"] for item in data["_embedded"]["items"]]
        return []
    except Exception as e:
        print(f"Ошибка при получении списка файлов: {e}")
        return []


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global OAUTH_TOKEN

        if OAUTH_TOKEN is None:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("""
                <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Вход - Загрузка на Яндекс.Диск</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                max-width: 500px;
                                margin: 50px auto;
                                padding: 20px;
                            }
                            h1 {
                                color: #333;
                            }
                            .form-group {
                                margin: 20px 0;
                            }
                            label {
                                display: block;
                                margin-bottom: 5px;
                                font-weight: bold;
                            }
                            input[type="text"] {
                                width: 100%;
                                padding: 10px;
                                border: 1px solid #ddd;
                                border-radius: 4px;
                                box-sizing: border-box;
                            }
                            button {
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px 20px;
                                border: none;
                                border-radius: 4px;
                                cursor: pointer;
                                font-size: 16px;
                            }
                            button:hover {
                                background-color: #45a049;
                            }
                            .info {
                                background-color: #e7f3fe;
                                border-left: 4px solid #2196F3;
                                padding: 10px;
                                margin: 20px 0;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Загрузка файлов на Яндекс.Диск</h1>
                        <div class="info">
                            <p>Для работы с Яндекс.Диском необходим OAuth токен.</p>
                            <p>Получить токен можно на странице:
                            <a href="https://yandex.ru/dev/disk/poligon" target="_blank">https://yandex.ru/dev/disk/poligon</a></p>
                        </div>
                        <form method="POST" action="/set_token">
                            <div class="form-group">
                                <label for="token">OAuth токен:</label>
                                <input type="text" id="token" name="token" required
                                       placeholder="Введите ваш OAuth токен">
                            </div>
                            <button type="submit">Войти</button>
                        </form>
                    </body>
                </html>
            """.encode('utf-8'))
            return

        # Если токен установлен, показываем список файлов
        uploaded_files = get_uploaded_files(OAUTH_TOKEN)

        def fname2html(fname):
            # Проверяем, загружен ли файл на Яндекс.Диск
            is_uploaded = fname in uploaded_files
            # Добавляем фоновый цвет, если файл загружен
            style = 'style="background-color: rgba(0, 200, 0, 0.25);"' if is_uploaded else ''
            return f"""
                <li {style} onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}}).then(() => location.reload())">
                    {fname} {'✓' if is_uploaded else ''}
                </li>
            """

        try:
            local_files = os.listdir("pdfs")
        except FileNotFoundError:
            local_files = []
            print("Папка pdfs не найдена")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>Загрузка файлов на Яндекс.Диск</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            max-width: 800px;
                            margin: 50px auto;
                            padding: 20px;
                        }}
                        h1 {{
                            color: #333;
                        }}
                        .header {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-bottom: 20px;
                        }}
                        .logout {{
                            background-color: #f44336;
                            color: white;
                            padding: 8px 16px;
                            border: none;
                            border-radius: 4px;
                            cursor: pointer;
                            text-decoration: none;
                            display: inline-block;
                        }}
                        .logout:hover {{
                            background-color: #da190b;
                        }}
                        ul {{
                            list-style-type: none;
                            padding: 0;
                        }}
                        li {{
                            padding: 15px;
                            margin: 5px 0;
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            cursor: pointer;
                            transition: all 0.3s;
                        }}
                        li:hover {{
                            background-color: #f0f0f0;
                            border-color: #999;
                        }}
                        .info {{
                            background-color: #e7f3fe;
                            border-left: 4px solid #2196F3;
                            padding: 10px;
                            margin: 20px 0;
                        }}
                        .legend {{
                            margin: 20px 0;
                            padding: 10px;
                            background-color: #f9f9f9;
                            border-radius: 4px;
                        }}
                        .legend span {{
                            margin-right: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>Файлы для загрузки на Яндекс.Диск</h1>
                        <form method="POST" action="/logout" style="margin: 0;">
                            <button type="submit" class="logout">Выйти</button>
                        </form>
                    </div>
                    <div class="legend">
                        <span>✓ - Файл уже загружен на Яндекс.Диск</span>
                        <span style="background-color: rgba(0, 200, 0, 0.25); padding: 5px;">Зелёный фон</span> - загружен
                    </div>
                    <div class="info">
                        <p>Нажмите на файл, чтобы загрузить его на Яндекс.Диск в папку "Backup".</p>
                    </div>
                    <ul>
                      {files}
                    </ul>
                </body>
            </html>
        """.format(files="\n".join(map(fname2html, local_files))).encode('utf-8'))

    def do_POST(self):
        global OAUTH_TOKEN

        if self.path == "/set_token":
            content_len = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_len).decode("utf-8")
            params = urllib.parse.parse_qs(post_data)
            if "token" in params:
                OAUTH_TOKEN = params["token"][0]
                print(f"Токен установлен: {OAUTH_TOKEN[:10]}...")

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if self.path == "/logout":
            OAUTH_TOKEN = None
            print("Токен сброшен")
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if self.path == "/upload":
            if OAUTH_TOKEN is None:
                self.send_response(403)
                self.end_headers()
                return

            content_len = int(self.headers.get('Content-Length'))
            fname = self.rfile.read(content_len).decode("utf-8")
            local_path = f"pdfs/{fname}"
            ya_path = f"Backup/{urllib.parse.quote(fname)}"

            try:
                resp = get(
                    f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
                    headers={"Authorization": f"OAuth {OAUTH_TOKEN}"}
                )
                print(f"Ответ от Яндекс.Диска: {resp.status_code}")
                print(resp.text)

                if resp.status_code == 200:
                    upload_url = json.loads(resp.text)["href"]
                    print(f"URL для загрузки: {upload_url}")

                    with open(local_path, 'rb') as f:
                        resp = put(upload_url, files={'file': (fname, f)})
                    print(f"Статус загрузки: {resp.status_code}")

                    self.send_response(200)
                    self.end_headers()
                else:
                    print(f"Ошибка получения URL загрузки: {resp.text}")
                    self.send_response(resp.status_code)
                    self.end_headers()
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                self.send_response(500)
                self.end_headers()


run(handler_class=HttpGetHandler)
