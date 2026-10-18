from pydantic import BaseModel, ConfigDict, Field


class EditorialCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    pais: str = Field(min_length=1, max_length=100)


class EditorialUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    pais: str | None = Field(default=None, min_length=1, max_length=100)


class EditorialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    pais: str
