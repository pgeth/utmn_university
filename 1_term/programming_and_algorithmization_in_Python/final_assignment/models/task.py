class Task:
  VALID_PRIORITIES = ("low", "normal", "high")

  def __init__(self, title, priority, is_done=False, task_id=None):
    self.id = task_id
    self.title = title
    self.priority = priority
    self.isDone = is_done

  def to_dict(self):
    return {"id": self.id, "title": self.title, "priority": self.priority, "isDone": self.isDone}

  @classmethod
  def from_dict(cls, data):
    return cls(data["title"], data["priority"], data.get("isDone", False), data.get("id"))
