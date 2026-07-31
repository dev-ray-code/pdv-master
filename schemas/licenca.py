from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LicencaBase(BaseModel):
    cliente_id: int

    plano: str

    codigo: Optional[str] = None

    status: str = "ATIVA"

    limite_computadores: int = 1
    limite_usuarios: int = 1

    data_ativacao: Optional[datetime] = None
    data_vencimento: Optional[datetime] = None


class LicencaCreate(LicencaBase):
    pass


class LicencaUpdate(BaseModel):
    plano: Optional[str] = None
    status: Optional[str] = None

    limite_computadores: Optional[int] = None
    limite_usuarios: Optional[int] = None

    data_ativacao: Optional[datetime] = None
    data_vencimento: Optional[datetime] = None


class LicencaResponse(LicencaBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True