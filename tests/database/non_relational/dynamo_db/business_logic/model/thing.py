class Thing:
    creation_instance: str

    def __init__(self, thing_id) -> None:
        self.creation_instance = thing_id

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return self.creation_instance == __o.creation_instance
        else:
            False
