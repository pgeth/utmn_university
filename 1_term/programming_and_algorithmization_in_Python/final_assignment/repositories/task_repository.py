import json
import os
from models.task import Task


class TaskRepository:
  def __init__(self, file_path="tasks.txt"):
    self.file_path = file_path
    self._tasks = []
    self._next_id = 1
    self._load()

  def _load(self):
    if not os.path.exists(self.file_path):
      return
    try:
      with open(self.file_path, "r", encoding="utf-8") as f:
        self._tasks = [Task.from_dict(item) for item in json.load(f)]
        if self._tasks:
          self._next_id = max(t.id for t in self._tasks) + 1
    except (json.JSONDecodeError, KeyError):
      pass

  def _save(self):
    with open(self.file_path, "w", encoding="utf-8") as f:
      json.dump([t.to_dict() for t in self._tasks], f, ensure_ascii=False, indent=2)

  def get_all(self):
    return self._tasks.copy()

  def get_by_id(self, task_id):
    return next((t for t in self._tasks if t.id == task_id), None)

  def add(self, task):
    task.id = self._next_id
    self._next_id += 1
    self._tasks.append(task)
    self._save()
    return task

  def update(self, task):
    for i, t in enumerate(self._tasks):
      if t.id == task.id:
        self._tasks[i] = task
        self._save()
        return True
    return False
