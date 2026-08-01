from typing import List

from fastapi import APIRouter, Depends, status, Body
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


@router.get(
    "/",
    response_model=List[LicencaResponse]
)
def listar_licencas(
    db: Session = Depends(get_db)
):
    return LicencaService.listar(db)


@router.get(
    "/{licenca_id}",
    response_model=LicencaResponse
)
def buscar_licenca(
    licenca_id: int,
    db: Session = Depends(get_db)
):
    return LicencaService.buscar(
        db,
        licenca_id
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def criar_licenca(
    dados: LicencaCreate,
    db: Session = Depends(get_db)
):
    return LicencaService.criar(
        db,
        dados
    )


@router.post("/validar")
def validar_licenca(
    dados: dict = Body(...),
    db: Session = Depends(get_db)
):
    return LicencaService.validar(
        db,
        dados.get("codigo")
    )


@router.put(
    "/{licenca_id}",
    response_model=LicencaResponse
)
def atualizar_licenca(
    licenca_id: int,
    dados: LicencaUpdate,
    db: Session = Depends(get_db)
):
    return LicencaService.atualizar(
        db,
        licenca_id,
        dados
    )


@router.delete(
    "/{licenca_id}"
)
def excluir_licenca(
    licenca_id: int,
    db: Session = Depends(get_db)
):
    return LicencaService.excluir(
        db,
        licenca_id
    )