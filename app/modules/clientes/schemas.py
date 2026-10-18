from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    email: EmailStr


class ClienteUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None


class PerfilCreate(BaseModel):
    telefono: str = Field(min_length=1, max_length=50)
    direccion: str = Field(min_length=1, max_length=250)


class PerfilRead(PerfilCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cliente_id: int


class ClienteRead(ClienteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    perfil: PerfilRead | None = None
