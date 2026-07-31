from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db

from schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)

from services.usuario_service import UsuarioService


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db)
):
    return UsuarioService.listar(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    return UsuarioService.buscar(db, usuario_id)


@router.post("/", response_model=UsuarioResponse)
def criar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return UsuarioService.criar(db, dados)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    return UsuarioService.atualizar(
        db,
        usuario_id,
        dados
    )


@router.delete("/{usuario_id}")
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    return UsuarioService.excluir(
        db,
        usuario_id
    )