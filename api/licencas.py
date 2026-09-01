from typing import List

from fastapi import APIRouter, Depends, Body, status

from sqlalchemy.orm import Session

from database.db import get_db
from api.admin_auth import verificar_admin_token

from schemas.licenca import (
    LicencaCreate,
    LicencaUpdate,
    LicencaResponse
)

from services.licenca_service import LicencaService


# Router PÚBLICO: só a validação de licença, que é chamada pelo próprio
# PDV instalado no cliente (não passa por login de admin).
router = APIRouter(
    prefix="/licencas",
    tags=["Licenças"]
)

# Router PROTEGIDO: tudo que é gestão/CRUD de licenças, uso exclusivo
# do painel admin.
router_admin = APIRouter(
    prefix="/licencas",
    tags=["Licenças (admin)"],
    dependencies=[Depends(verificar_admin_token)]
)


# ==========================================================
# LISTAR LICENÇAS (admin)
# ==========================================================

@router_admin.get(
    "/",
    response_model=List[LicencaResponse]
)
def listar(
    db: Session = Depends(get_db)
):

    return LicencaService.listar(db)


# ==========================================================
# BUSCAR LICENÇA (admin)
# ==========================================================

@router_admin.get(
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
# CRIAR LICENÇA (admin)
# ==========================================================

@router_admin.post(
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
# VALIDAR LICENÇA (público — chamado pelo PDV do cliente)
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
# ATUALIZAR LICENÇA (admin)
# ==========================================================

@router_admin.put(
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
# EXCLUIR LICENÇA (admin)
# ==========================================================

@router_admin.delete("/{licenca_id}")
def excluir(
    licenca_id: int,
    db: Session = Depends(get_db)
):

    return LicencaService.excluir(
        db,
        licenca_id
    )


# ==========================================================
# REDEFINIR SENHA DO USUÁRIO DA LICENÇA (admin)
# Gera uma nova senha aleatória para o cliente usar no PDV.
# Retorna a nova senha em texto para o admin copiar e enviar.
# ==========================================================

@router_admin.post("/{licenca_id}/redefinir-senha")
def redefinir_senha(
    licenca_id: int,
    db: Session = Depends(get_db)
):

    return LicencaService.redefinir_senha(
        db,
        licenca_id
    )