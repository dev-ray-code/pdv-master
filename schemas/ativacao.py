from pydantic import BaseModel
from typing import Optional


class AtivacaoRequest(BaseModel):
    codigo_licenca: str

    machine_id: str

    nome_computador: str

    tipo: str

    sistema_operacional: str

    versao_pdv: str

    ip: Optional[str] = None

    mac: Optional[str] = None

    serial: Optional[str] = None


class AtivacaoResponse(BaseModel):

    autorizado: bool

    mensagem: str

    cliente_id: Optional[int] = None

    licenca_id: Optional[int] = None

    empresa: Optional[str] = None

    plano: Optional[str] = None

    status: Optional[str] = None

    validade: Optional[str] = None

    sincronizar: bool = True

    baixar_atualizacao: bool = False

    versao_minima: str = "1.0.0"