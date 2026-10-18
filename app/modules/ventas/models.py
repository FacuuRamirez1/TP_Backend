from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, Column, ForeignKey, Index, Numeric
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.clientes.models import Cliente
    from app.modules.libros.models import Libro


class Venta(SQLModel, table=True):
    __tablename__ = "venta"
    __table_args__ = (
        CheckConstraint("total >= 0", name="ck_venta_total_no_negativo"),
        Index("ix_venta_cliente_id", "cliente_id"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id", nullable=False)
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    total: Decimal = Field(sa_column=Column(Numeric(12, 2), nullable=False))
    cliente: "Cliente" = Relationship(back_populates="ventas")
    renglones: list["RenglonVenta"] = Relationship(back_populates="venta", cascade_delete=True)


class RenglonVenta(SQLModel, table=True):
    __tablename__ = "renglon_venta"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_renglon_cantidad_positivo"),
        CheckConstraint("precio_unitario > 0", name="ck_renglon_precio_positivo"),
        Index("ix_renglon_venta_id", "venta_id"),
        Index("ix_renglon_libro_id", "libro_id"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    venta_id: int = Field(foreign_key="venta.id", nullable=False)
    libro_id: int = Field(foreign_key="libro.id", nullable=False)
    cantidad: int = Field(nullable=False, gt=0)
    precio_unitario: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    venta: Venta = Relationship(back_populates="renglones")
    libro: "Libro" = Relationship(back_populates="renglones")

    @property
    def titulo(self) -> str:
        return self.libro.titulo
