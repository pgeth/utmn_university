"""HTTP-сервер для управления задачами."""

import json
import re
from http.server import BaseHTTPRequestHandler

from services.task_service import TaskService


class TaskHTTPHandler(BaseHTTPRequestHandler):
  task_service: TaskService = None

  def _read_json_body(self) -> dict | None:
    length = int(self.headers.get("Content-Length", 0))
    if length == 0:
      return None
    try:
      raw = self.rfile.read(length)
      return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
      return None

  def _send_json(self, data, status: int = 200) -> None:
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    self.send_response(status)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.send_header("Content-Length", str(len(payload)))
    self.end_headers()
    self.wfile.write(payload)

  def _send_empty(self, status=200):
    self.send_response(status)
    self.send_header("Content-Length", "0")
    self.end_headers()

  def _send_error(self, status, message):
    self._send_json({"error": message}, status)

  def _parse_task_id_from_complete_path(self, path: str) -> int | None:
    """Извлечь ID задачи из пути /tasks/{id}/complete."""
    match = re.match(r"^/tasks/(\d+)/complete$", path)
    if match:
        return int(match.group(1))
    return None

  def do_GET(self) -> None:
    if self.path == "/tasks":
        self._handle_get_all_tasks()
    else:
        self._send_error(404, "Not found")

  def do_POST(self) -> None:
    if self.path == "/tasks":
      self._handle_create_task()
    else:
      task_id = self._parse_task_id_from_complete_path(self.path)
      if task_id is not None:
        self._handle_complete_task(task_id)
      else:
        self._send_error(404, "Not found")

  def _handle_get_all_tasks(self) -> None:
    """GET /tasks - получить список всех задач."""
    tasks = self.task_service.get_all_tasks()
    result = [task.to_dict() for task in tasks]
    self._send_json(result)

  def _handle_create_task(self) -> None:
    """POST /tasks - создать новую задачу."""
    data = self._read_json_body()

    if not data:
      self._send_error(400, "Request body is required")
      return

    title = data.get("title")
    priority = data.get("priority")

    if not title:
      self._send_error(400, "Field 'title' is required")
      return

    if not priority:
      self._send_error(400, "Field 'priority' is required")
      return

    task = self.task_service.create_task(title, priority)

    if task is None:
      self._send_error(400, "Invalid priority. Must be: low, normal, high")
      return

    self._send_json(task.to_dict(), status=201)

  def _handle_complete_task(self, task_id: int) -> None:
    """POST /tasks/{id}/complete - отметить задачу выполненной."""
    success = self.task_service.complete_task(task_id)
    if success:
      self._send_empty(200)
    else:
      self._send_empty(404)

  def log_message(self, format: str, *args) -> None:
    """Метод для логов"""
    print(f"[{self.log_date_time_string()}] {args[0]}")
