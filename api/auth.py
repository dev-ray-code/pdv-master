import os
import time
from datetime import datetime, timedelta
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import get_db
from database.models import Usuario

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

# ATENÇÃO: em produção (Render) defina a variável de ambiente SECRET_KEY
# com um valor aleatório e longo. Se ela não existir, o servidor ainda
# sobe (para não quebrar o deploy), mas usando uma chave gerada na hora
# do boot — o que já é bem melhor do que ter a chave fixa no código e
# versionada no Git. Configure a variável assim que possível:
#   Render > seu serviço > Environment > Add Environment Variable
#   SECRET_KEY = <string aleatória longa, ex: gerada com secrets.token_hex(32)>
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    import secrets as _secrets
    SECRET_KEY = _secrets.token_hex(32)
    print(
        "[AVISO] Variável de ambiente SECRET_KEY não definida. "
        "Usando uma chave temporária gerada no boot — todos os tokens "
        "emitidos serão invalidados a cada reinício do servidor. "
        "Defina SECRET_KEY no ambiente do Render."
    )

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# --- Rate limiting simples em memória para o /auth/login e /admin/login ---
# Isto NÃO substitui um rate limit de verdade (ex: Redis) em produção com
# múltiplas instâncias, mas já impede força bruta trivial num único
# processo. Cada reinício do servidor zera os contadores.
_tentativas_login: Dict[str, List[float]] = {}
_JANELA_SEGUNDOS = 300  # 5 minutos
_MAX_TENTATIVAS = 5


def checar_rate_limit(chave: str):
    agora = time.time()
    tentativas = _tentativas_login.get(chave, [])
    tentativas = [t for t in tentativas if agora - t < _JANELA_SEGUNDOS]
    if len(tentativas) >= _MAX_TENTATIVAS:
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas de login. Aguarde alguns minutos e tente novamente."
        )
    tentativas.append(agora)
    _tentativas_login[chave] = tentativas


def limpar_rate_limit(chave: str):
    _tentativas_login.pop(chave, None)


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
    request: Request,
    db: Session = Depends(get_db)
):
    # chave do rate limit: IP + usuário tentado, para não travar a loja
    # inteira por causa de uma tentativa errada de outro cliente
    chave_limite = f"{request.client.host if request.client else 'desconhecido'}:{dados.usuario}"
    checar_rate_limit(chave_limite)

    usuario = db.query(Usuario).filter(
        Usuario.usuario == dados.usuario
    ).first()

    # Mensagem sempre igual, propositalmente: não dá para saber, pela
    # resposta, se o usuário existe ou se foi a senha que errou. Isso
    # evita enumeração de usuários válidos por tentativa e erro.
    credenciais_invalidas = HTTPException(
        status_code=401,
        detail="Usuário ou senha inválidos."
    )

    if not usuario:
        raise credenciais_invalidas

    if not verificar_senha(
        dados.senha,
        usuario.senha_hash
    ):
        raise credenciais_invalidas

    limpar_rate_limit(chave_limite)

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