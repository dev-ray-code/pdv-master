from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db

from schemas.dispositivo import (
    DispositivoConectar,
    DispositivoResponse
)

from services.dispositivo_service import DispositivoService

router = APIRouter(
    prefix="/dispositivos",
    tags=["Dispositivos"]
)


@router.get(
    "/",
    response_model=List[DispositivoResponse]
)
def listar_dispositivos(
    db: Session = Depends(get_db)
):
    return DispositivoService.listar(db)


@router.post("/conectar")
def conectar_dispositivo(
    dados: DispositivoConectar,
    db: Session = Depends(get_db)
):
    return DispositivoService.conectar(
        db,
        dados
    )


@router.post("/{dispositivo_id}/bloquear")
def bloquear_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db)
):
    return DispositivoService.bloquear(
        db,
        dispositivo_id
    )


@router.post("/{dispositivo_id}/desbloquear")
def desbloquear_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db)
):
    return DispositivoService.desbloquear(
        db,
        dispositivo_id
    )


@router.delete("/{dispositivo_id}")
def excluir_dispositivo(
    dispositivo_id: int,
    db: Session = Depends(get_db)
):
    return DispositivoService.excluir(
        db,
        dispositivo_id
    )