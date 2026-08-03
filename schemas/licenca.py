from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class LicencaBase(BaseModel):

    cliente_id: int

    plano: str = "ANUAL"

    validade: Optional[date] = None

    limite_computadores: int = 1


class LicencaCreate(LicencaBase):
    pass


class LicencaUpdate(BaseModel):

    plano: Optional[str] = None

    status: Optional[str] = None

    validade: Optional[date] = None

    limite_computadores: Optional[int] = None


class LicencaResponse(BaseModel):

    id: int

    cliente_id: int

    chave: str

    plano: str

    status: str

    validade: Optional[date]

    limite_computadores: int

    criado_em: datetime

    class Config:
        from_attributes = True