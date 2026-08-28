from typing import List

from fastapi import APIRouter, Depends, Body, status

from sqlalchemy.orm import Session

from database.db import get_db

from schemas.licenca import (
    LicencaCreate,
    LicencaUpdate,
    LicencaResponse
)

from services.licenca_service import LicencaService


router = APIRouter(
    prefix="/licencas",
    tags=["Licenças"]
)


# ==========================================================
# LISTAR LICENÇAS
# ==========================================================

@router.get(
    "/",
    response_model=List[LicencaResponse]
)
def listar(
    db: Session = Depends(get_db)
):

    return LicencaService.listar(db)


# ==========================================================
# BUSCAR LICENÇA
# ==========================================================

@router.get(
    "/{licenca_id}",
    response_model=LicencaResponse
)
def buscar(
    licenca_id: int,
    db: Session = Depends(get_db)
):

    return LicencaService.buscar(
        db,
        licenca_id
    )


# ==========================================================
# CRIAR LICENÇA
# ==========================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def criar(
    dados: LicencaCreate,
    db: Session = Depends(get_db)
):

    return LicencaService.criar(
        db,
        dados
    )


# ==========================================================
# VALIDAR LICENÇA
# ==========================================================

@router.post("/validar")
def validar(
    dados: dict = Body(...),
    db: Session = Depends(get_db)
):

    codigo = dados.get("codigo")

    if not codigo:

        return {
            "autorizado": False,
            "mensagem": "Código da licença não informado."
        }

    return LicencaService.validar(
        db,
        codigo
    )


# ==========================================================
# ATUALIZAR LICENÇA
# ==========================================================

@router.put(
    "/{licenca_id}",
    response_model=LicencaResponse
)
def atualizar(
    licenca_id: int,
    dados: LicencaUpdate,
    db: Session = Depends(get_db)
):

    return LicencaService.atualizar(
        db,
        licenca_id,
        dados
    )


# ==========================================================
# EXCLUIR LICENÇA
# ==========================================================

@router.delete("/{licenca_id}")
def excluir(
    licenca_id: int,
    db: Session = Depends(get_db)
):

    return LicencaService.excluir(
        db,
        licenca_id
    )