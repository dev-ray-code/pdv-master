from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    empresa: str
    nome: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    empresa: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True