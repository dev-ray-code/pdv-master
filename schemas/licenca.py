from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================================
# LICENÇA BASE
# ==========================================================

class LicencaBase(BaseModel):

    cliente_id: int

    plano: str = "ANUAL"

    validade: Optional[date] = None

    limite_computadores: int = 1


# ==========================================================
# CRIAR LICENÇA
# ==========================================================

class LicencaCreate(LicencaBase):
    pass


# ==========================================================
# ATUALIZAR LICENÇA
# ==========================================================

class LicencaUpdate(BaseModel):

    plano: Optional[str] = None

    status: Optional[str] = None

    validade: Optional[date] = None

    limite_computadores: Optional[int] = None


# ==========================================================
# RESPOSTA
# ==========================================================

class LicencaResponse(BaseModel):

    id: int

    cliente_id: int

    # Nome da empresa do cliente
    empresa: Optional[str] = None

    # Nome do cliente
    usuario: Optional[str] = None

    chave: str

    plano: str

    status: str

    validade: Optional[date] = None

    limite_computadores: int

    criado_em: datetime

    model_config = ConfigDict(
        from_attributes=True
    )