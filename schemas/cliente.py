from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    empresa: str
    nome: str

    usuario: str

    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: EmailStr
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    plano: str = "MENSAL"
    status: str = "ATIVO"

    validade: Optional[datetime] = None

    limite_computadores: int = 1
    limite_usuarios: int = 1


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    empresa: Optional[str] = None
    nome: Optional[str] = None

    usuario: Optional[str] = None

    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

    plano: Optional[str] = None
    status: Optional[str] = None

    validade: Optional[datetime] = None

    limite_computadores: Optional[int] = None
    limite_usuarios: Optional[int] = None


class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True