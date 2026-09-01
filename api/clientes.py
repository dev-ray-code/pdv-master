from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.db import get_db
from api.admin_auth import verificar_admin_token

from schemas.cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse
)

from services.cliente_service import ClienteService

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    # Todas as rotas deste arquivo são de uso exclusivo do painel admin,
    # então exigimos o token de admin para o router inteiro.
    dependencies=[Depends(verificar_admin_token)]
)


@router.get(
    "/",
    response_model=List[ClienteResponse]
)
def listar_clientes(
    db: Session = Depends(get_db)
):
    return ClienteService.listar(db)


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return ClienteService.buscar(
        db,
        cliente_id
    )


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_cliente(
    dados: ClienteCreate,
    db: Session = Depends(get_db)
):
    return ClienteService.criar(
        db,
        dados
    )


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    db: Session = Depends(get_db)
):
    return ClienteService.atualizar(
        db,
        cliente_id,
        dados
    )


@router.delete("/{cliente_id}")
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return ClienteService.excluir(
        db,
        cliente_id
    )