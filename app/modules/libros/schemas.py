from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Role = Literal["autor", "coautor", "traductor", "ilustrador"]


class AutorLibroCreate(BaseModel):
    autor_id: int = Field(gt=0)
    rol: Role
    orden: int = Field(ge=1)


class AutorInLibro(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    nacionalidad: str


class AutorLibroRead(AutorLibroCreate):
    model_config = ConfigDict(from_attributes=True)
    autor: AutorInLibro


class LibroInAutor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    isbn: str
    titulo: str


class LibroAutorRead(AutorLibroCreate):
    model_config = ConfigDict(from_attributes=True)
    libro: LibroInAutor
class LibroCreate(BaseModel):
    isbn: str = Field(min_length=1, max_length=30)
    titulo: str = Field(min_length=1, max_length=250)
    precio: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(ge=0)
    editorial_id: int = Field(gt=0)
    genero_id: int | None = Field(default=None, gt=0)
    autores: list[AutorLibroCreate] = Field(default_factory=list)


class LibroUpdate(BaseModel):
    isbn: str | None = Field(default=None, min_length=1, max_length=30)
    titulo: str | None = Field(default=None, min_length=1, max_length=250)
    precio: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    editorial_id: int | None = Field(default=None, gt=0)
    genero_id: int | None = Field(default=None, gt=0)


class EditorialInLibro(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    pais: str


class GeneroInLibro(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str


class LibroListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    isbn: str
    titulo: str
    precio: Decimal
    stock: int


class LibroRead(LibroListRead):
    editorial: EditorialInLibro
    genero: GeneroInLibro | None
    autorias: list[AutorLibroRead]
