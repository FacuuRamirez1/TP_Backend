from pydantic import BaseModel


class HealthRead(BaseModel):
    estado: str
