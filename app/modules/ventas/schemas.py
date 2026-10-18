from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from app.modules.clientes.schemas import ClienteRead


class RenglonCreate(BaseModel):
    libro_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class VentaCreate(BaseModel):
    cliente_id: int = Field(gt=0)
    renglones: list[RenglonCreate] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_books(self):
        ids = [item.libro_id for item in self.renglones]
        if len(ids) != len(set(ids)):
            raise ValueError("Una venta no puede repetir un libro en sus renglones")
        return self


class RenglonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    libro_id: int
    titulo: str
    cantidad: int
    precio_unitario: Decimal

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad


class VentaListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cliente_id: int
    fecha: datetime
    total: Decimal


class VentaRead(VentaListRead):
    cliente: ClienteRead
    renglones: list[RenglonRead]
