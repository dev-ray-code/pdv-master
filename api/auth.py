from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import get_db
from database.models import Usuario

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

SECRET_KEY = "PDV_STORE_MASTER_2026"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(
    senha: str,
    senha_hash: str
):
    return pwd_context.verify(
        senha,
        senha_hash
    )


def criar_token(dados: dict):

    payload = dados.copy()

    payload["exp"] = (
        datetime.utcnow()
        + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


class LoginRequest(BaseModel):
    usuario: str
    senha: str


@router.post("/login")
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.usuario == dados.usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado."
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Senha inválida."
        )

    token = criar_token(
        {
            "usuario_id": usuario.id,
            "cliente_id": usuario.cliente_id,
            "perfil": usuario.perfil
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario.usuario,
        "cliente_id": usuario.cliente_id,
        "perfil": usuario.perfil
    }