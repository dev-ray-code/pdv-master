from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Cliente, Licenca

from schemas.ativacao import (
    AtivacaoRequest,
    AtivacaoResponse
)

from services.dispositivo_service import DispositivoService

router = APIRouter(
    prefix="/windows",
    tags=["Windows"]
)


@router.get("/")
def status():
    return {
        "status": "online",
        "servidor": "PDV Store Server"
    }


@router.post(
    "/ativar",
    response_model=AtivacaoResponse
)
def ativar_pdv(
    dados: AtivacaoRequest,
    db: Session = Depends(get_db)
):

    resultado = DispositivoService.conectar(
        db,
        dados
    )

    licenca = db.query(Licenca).filter(
        Licenca.id == resultado["licenca_id"]
    ).first()

    cliente = db.query(Cliente).filter(
        Cliente.id == resultado["cliente_id"]
    ).first()

    return AtivacaoResponse(
        autorizado=True,
        mensagem=resultado["mensagem"],
        cliente_id=cliente.id,
        licenca_id=licenca.id,
        empresa=cliente.empresa,
        plano=licenca.plano,
        status=licenca.status,
        validade=str(licenca.data_vencimento)
        if licenca.data_vencimento else None,
        sincronizar=True,
        baixar_atualizacao=False,
        versao_minima="1.0.0"
    )