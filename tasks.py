from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    priority: str
    isDone: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "isDone": self.isDone
        }