class Task:
    description: str

    def __init__(self, task_description) -> None:
        self.description = task_description

    def __eq__(self, other) -> bool:
        return self.description == other.description \
            if isinstance(other, self.__class__) else  False
