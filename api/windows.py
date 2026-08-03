from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from services.dispositivo_service import DispositivoService
from schemas.dispositivo import DispositivoConectar

router = APIRouter(
    prefix="/windows",
    tags=["Windows"]
)


@router.get("/")
def status():
    return {
        "status": "online",
        "servidor": "PDV Store Master"
    }


@router.post("/ativar")
def ativar(
    dados: DispositivoConectar,
    db: Session = Depends(get_db)
):
    return DispositivoService.conectar(
        db,
        dados
    )