"""Тесты для API задач."""

import os
import sys
import pytest
import requests
import threading
import time
from http.server import HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repositories.task_repository import TaskRepository
from services.task_service import TaskService
from server import TaskHTTPHandler


@pytest.fixture(scope="session")
def server():
  """Запуск тестового сервера."""
  host = "127.0.0.1"
  port = 8889

  test_file = os.path.join(os.path.dirname(__file__), "test_tasks.txt")
  repository = TaskRepository(test_file)
  task_service = TaskService(repository)
  TaskHTTPHandler.task_service = task_service

  httpd = HTTPServer((host, port), TaskHTTPHandler)
  server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
  server_thread.start()
  time.sleep(0.5)

  try:
    yield f"http://{host}:{port}"
  finally:
    httpd.shutdown()
    httpd.server_close()
    if os.path.exists(test_file):
        os.remove(test_file)


@pytest.fixture(autouse=True)
def reset_data(server):
  """Очистка данных перед каждым тестом."""
  test_file = os.path.join(os.path.dirname(__file__), "test_tasks.txt")
  TaskHTTPHandler.task_service.repository._tasks = []
  TaskHTTPHandler.task_service.repository._next_id = 1
  if os.path.exists(test_file):
    os.remove(test_file)
  yield


class TestCreateTask:
  """Тесты создания задач (POST /tasks)."""

  def test_create_task_success(self, server):
    """Успешное создание задачи."""
    response = requests.post(
      f"{server}/tasks",
      json={"title": "Gym", "priority": "low"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Gym"
    assert data["priority"] == "low"
    assert data["isDone"] == False

  def test_create_task_without_title(self, server):
    """Создание задачи без title."""
    response = requests.post(
      f"{server}/tasks",
      json={"priority": "low"}
    )
    assert response.status_code == 400

  def test_create_task_without_priority(self, server):
    """Создание задачи без priority."""
    response = requests.post(
      f"{server}/tasks",
      json={"title": "Test"}
    )
    assert response.status_code == 400


class TestGetTasks:
  """Тесты получения задач (GET /tasks)."""
  def test_get_empty_list(self, server):
    """Получение пустого списка задач."""
    response = requests.get(f"{server}/tasks")

    assert response.status_code == 200
    assert response.json() == []

  def test_get_all_tasks(self, server):
    """Получение списка всех задач."""
    requests.post(f"{server}/tasks", json={"title": "Task 1", "priority": "low"})
    requests.post(f"{server}/tasks", json={"title": "Task 2", "priority": "high"})

    response = requests.get(f"{server}/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


class TestCompleteTask:
  """Тесты отметки выполнения (POST /tasks/{id}/complete)."""

  def test_complete_task_success(self, server):
    """Успешная отметка задачи как выполненной."""
    create_resp = requests.post(
      f"{server}/tasks",
      json={"title": "Gym", "priority": "low"}
    )
    task_id = create_resp.json()["id"]

    response = requests.post(f"{server}/tasks/{task_id}/complete")

    assert response.status_code == 200

    get_resp = requests.get(f"{server}/tasks")
    assert get_resp.json()[0]["isDone"] == True

  def test_complete_task_not_found(self, server):
    """Отметка несуществующей задачи возвращает 404."""
    response = requests.post(f"{server}/tasks/999/complete")

    assert response.status_code == 404
