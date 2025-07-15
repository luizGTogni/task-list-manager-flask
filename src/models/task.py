class Task:
    def __init__(self, id: int, title: str, description: str, completed = False) -> None:
        self._id = id
        self.title = title
        self.description = description
        self._completed = completed

    @property
    def completed(self):
        return self._completed
    
    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }