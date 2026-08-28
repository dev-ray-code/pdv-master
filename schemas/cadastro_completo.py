from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# CADASTRO COMPLETO
# ==========================================================

class CadastroCompletoCreate(BaseModel):

    # ======================================================
    # CLIENTE
    # ======================================================

    empresa: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    nome: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    telefone: Optional[str] = None

    endereco: Optional[str] = None

    # ======================================================
    # LICENÇA
    # ======================================================

    plano: str = "ANUAL"

    validade: Optional[date] = None

    limite_computadores: int = Field(
        default=1,
        ge=1
    )


# ==========================================================
# RESPOSTA
# ==========================================================

class CadastroCompletoResponse(BaseModel):

    cliente_id: int

    empresa: str

    nome: str

    usuario: str

    senha: str

    licenca_id: int

    chave: str

    plano: str

    status: str

    validade: Optional[date]

    limite_computadores: int