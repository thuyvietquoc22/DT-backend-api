from pydantic import BaseModel


class PassageCapacityStatus(BaseModel):
    name: str
    keyname: str
    value: float

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value
