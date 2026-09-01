"""
Autenticação do PAINEL ADMINISTRATIVO (dashboard/clientes/licenças).

Isto é separado do /auth/login, que é o login usado pelo PDV dos seus
clientes. Aqui é só para você (dono do sistema) acessar o painel de
gestão de licenças.

CONFIGURAÇÃO OBRIGATÓRIA NO RENDER (Environment):
  ADMIN_USUARIO         -> seu usuário de admin, ex: "admin"
  ADMIN_SENHA_HASH      -> hash bcrypt da sua senha (veja como gerar abaixo)
  SECRET_KEY            -> já deve existir (usado também pelo /auth)

Para gerar o hash da sua senha de admin, rode uma vez localmente:

    python -c "from passlib.context import CryptContext; \
c = CryptContext(schemes=['bcrypt']); print(c.hash('SUA_SENHA_AQUI'))"

e copie o resultado para a variável ADMIN_SENHA_HASH no Render.
NUNCA coloque a senha em texto puro numa variável de ambiente nem no
código — sempre o hash.

Se as variáveis não estiverem configuradas, o servidor sobe mesmo assim
(para não quebrar o deploy) mas usa um usuário/senha padrão SÓ PARA
DESENVOLVIMENTO LOCAL (admin / admin123) e imprime um aviso bem visível
no log. Não deixe isso acontecer em produção.
"""

import os
import time
from datetime import datetime, timedelta

from fastapi import APIRouter, Header, HTTPException, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from api.auth import SECRET_KEY, ALGORITHM, checar_rate_limit, limpar_rate_limit

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_USUARIO = os.getenv("ADMIN_USUARIO")
ADMIN_SENHA_HASH = os.getenv("ADMIN_SENHA_HASH")

if not ADMIN_USUARIO or not ADMIN_SENHA_HASH:
    ADMIN_USUARIO = ADMIN_USUARIO or "admin"
    ADMIN_SENHA_HASH = ADMIN_SENHA_HASH or pwd_context.hash("admin123")
    print(
        "=" * 70 + "\n"
        "[AVISO IMPORTANTE] ADMIN_USUARIO / ADMIN_SENHA_HASH não configurados.\n"
        "Usando credenciais padrão de DESENVOLVIMENTO: admin / admin123\n"
        "Configure as variáveis de ambiente no Render antes de ir para produção!\n"
        + "=" * 70
    )

ADMIN_TOKEN_EXPIRE_HOURS = 12


class AdminLoginRequest(BaseModel):
    usuario: str
    senha: str


def criar_token_admin():
    payload = {
        "perfil": "admin",
        "exp": datetime.utcnow() + timedelta(hours=ADMIN_TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login_admin(dados: AdminLoginRequest, request: Request):
    chave_limite = f"admin:{request.client.host if request.client else 'desconhecido'}"
    checar_rate_limit(chave_limite)

    credenciais_invalidas = HTTPException(
        status_code=401,
        detail="Usuário ou senha inválidos."
    )

    if dados.usuario != ADMIN_USUARIO:
        raise credenciais_invalidas

    if not pwd_context.verify(dados.senha, ADMIN_SENHA_HASH):
        raise credenciais_invalidas

    limpar_rate_limit(chave_limite)

    token = criar_token_admin()
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def verificar_admin_token(authorization: str = Header(None)):
    """
    Dependency para proteger rotas administrativas.
    Uso: adicione `dependencies=[Depends(verificar_admin_token)]` no
    APIRouter (ou no endpoint específico) que deve exigir login de admin.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Não autenticado. Faça login no painel."
        )

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Sessão inválida ou expirada. Faça login novamente."
        )

    if payload.get("perfil") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso restrito ao administrador."
        )

    return payload