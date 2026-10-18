from pydantic import BaseModel, ConfigDict, Field


class AutorCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    nacionalidad: str = Field(min_length=1, max_length=100)


class AutorUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    nacionalidad: str | None = Field(default=None, min_length=1, max_length=100)


class AutorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    nacionalidad: str
