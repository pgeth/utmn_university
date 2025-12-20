"""
Эндпоинты сервера:
POST /tasks               - создать задачу
GET  /tasks               - получить все задачи
POST /tasks/{id}/complete - отметить выполненной
"""
import os
import sys
from http.server import HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repositories.task_repository import TaskRepository
from services.task_service import TaskService
from server import TaskHTTPHandler


def run(host="127.0.0.1", port=8000):
  repository = TaskRepository(os.path.join(os.path.dirname(__file__), "tasks.txt"))
  TaskHTTPHandler.task_service = TaskService(repository)

  server = HTTPServer((host, port), TaskHTTPHandler)
  print(f"Сервер запущен: http://{host}:{port}")

  try:
    server.serve_forever()
  except KeyboardInterrupt:
    server.server_close()


run()
