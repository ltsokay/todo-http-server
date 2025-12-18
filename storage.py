import json
from pathlib import Path
from typing import List
from tasks import Task


class Storage:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename

    def save(self, tasks: List[Task]):
        data = [t.to_dict() for t in tasks]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self) -> List[Task]:
        if not Path(self.filename).exists():
            return []

        with open(self.filename, "r") as f:
            data = json.load(f)

        return [Task(**item) for item in data]
