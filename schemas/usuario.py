from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    cliente_id: int
    usuario: str = Field(..., min_length=3, max_length=100)
    nome: str
    email: EmailStr
    perfil: str = "ADMIN"
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=4)


class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    perfil: Optional[str] = None
    ativo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    ultimo_login: Optional[datetime] = None
    criado_em: datetime

    class Config:
        from_attributes = True