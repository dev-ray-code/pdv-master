from typing import Optional

from pydantic import BaseModel


# ==========================================================
# CLIENTE BASE
# ==========================================================

class ClienteBase(BaseModel):

    empresa: str

    nome: str

    telefone: Optional[str] = None

    endereco: Optional[str] = None


# ==========================================================
# CRIAR CLIENTE
# ==========================================================

class ClienteCreate(ClienteBase):
    pass


# ==========================================================
# ATUALIZAR CLIENTE
# ==========================================================

class ClienteUpdate(BaseModel):

    empresa: Optional[str] = None

    nome: Optional[str] = None

    telefone: Optional[str] = None

    endereco: Optional[str] = None


# ==========================================================
# RESPOSTA
# ==========================================================

class ClienteResponse(ClienteBase):

    id: int

    criado_em: object

    class Config:

        from_attributes = True