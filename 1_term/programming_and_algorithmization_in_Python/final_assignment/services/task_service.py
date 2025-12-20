from models.task import Task

class TaskService:
  def __init__(self, repository):
    self.repository = repository

  def create_task(self, title, priority):
    if priority not in Task.VALID_PRIORITIES:
      return None
    return self.repository.add(Task(title, priority))

  def get_all_tasks(self):
    return self.repository.get_all()

  def complete_task(self, task_id):
    task = self.repository.get_by_id(task_id)
    if not task:
      return False
    task.isDone = True
    return self.repository.update(task)
