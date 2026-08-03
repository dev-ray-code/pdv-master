from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DispositivoBase(BaseModel):
    cliente_id: int
    licenca_id: int

    machine_id: str
    nome_computador: str

    tipo: str
    sistema_operacional: str
    versao_pdv: str


class DispositivoCreate(DispositivoBase):
    pass


class DispositivoConectar(BaseModel):
    usuario: str
    senha: str

    machine_id: str
    nome_computador: str

    tipo: str
    sistema_operacional: str
    versao_pdv: str


class DispositivoUpdate(BaseModel):
    nome_computador: Optional[str] = None
    sistema_operacional: Optional[str] = None
    versao_pdv: Optional[str] = None
    status: Optional[str] = None


class DispositivoResponse(DispositivoBase):
    id: int

    status: str
    ultimo_acesso: datetime

    class Config:
        from_attributes = True