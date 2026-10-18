from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, Column, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.autores.models import Autor
    from app.modules.editoriales.models import Editorial
    from app.modules.generos.models import Genero
    from app.modules.ventas.models import RenglonVenta


class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    __table_args__ = (
        CheckConstraint("precio > 0", name="ck_libro_precio_positivo"),
        CheckConstraint("stock >= 0", name="ck_libro_stock_no_negativo"),
        Index("ix_libro_editorial_id", "editorial_id"),
        Index("ix_libro_genero_id", "genero_id"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    isbn: str = Field(nullable=False, unique=True, max_length=30)
    titulo: str = Field(nullable=False, max_length=250)
    precio: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    stock: int = Field(nullable=False, ge=0)
    editorial_id: int = Field(foreign_key="editorial.id", nullable=False)
    genero_id: Optional[int] = Field(default=None, foreign_key="genero.id")
    editorial: "Editorial" = Relationship(back_populates="libros")
    genero: Optional["Genero"] = Relationship(back_populates="libros")
    autorias: list["LibroAutor"] = Relationship(back_populates="libro", cascade_delete=True)
    renglones: list["RenglonVenta"] = Relationship(back_populates="libro")


class LibroAutor(SQLModel, table=True):
    __tablename__ = "libro_autor"
    __table_args__ = (
        CheckConstraint("orden >= 1", name="ck_libro_autor_orden_positivo"),
        CheckConstraint("rol IN ('autor', 'coautor', 'traductor', 'ilustrador')", name="ck_libro_autor_rol"),
        Index("ix_libro_autor_libro_id", "libro_id"),
        Index("ix_libro_autor_autor_id", "autor_id"),
    )
    libro_id: int = Field(foreign_key="libro.id", primary_key=True)
    autor_id: int = Field(foreign_key="autor.id", primary_key=True)
    rol: str = Field(sa_column=Column(String(20), nullable=False))
    orden: int = Field(nullable=False, ge=1)
    libro: Libro = Relationship(back_populates="autorias")
    autor: "Autor" = Relationship(back_populates="autorias")