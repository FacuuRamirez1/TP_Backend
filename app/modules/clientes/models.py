from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.ventas.models import Venta


class Cliente(SQLModel, table=True):
    __tablename__ = "cliente"
    __table_args__ = (Index("ix_cliente_email", "email"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, max_length=150)
    email: str = Field(nullable=False, unique=True, max_length=254)
    perfil: Optional["PerfilCliente"] = Relationship(back_populates="cliente", cascade_delete=True)
    ventas: list["Venta"] = Relationship(back_populates="cliente")


class PerfilCliente(SQLModel, table=True):
    __tablename__ = "perfil_cliente"
    __table_args__ = (Index("ix_perfil_cliente_cliente_id", "cliente_id"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id", nullable=False, unique=True)
    telefono: str = Field(nullable=False, max_length=50)
    direccion: str = Field(nullable=False, max_length=250)
    cliente: Cliente = Relationship(back_populates="perfil")
