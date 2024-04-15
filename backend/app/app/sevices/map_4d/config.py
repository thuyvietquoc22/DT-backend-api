from pydantic import BaseModel


class Map4DConfig(BaseModel):
    api_key: str

