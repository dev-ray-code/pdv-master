from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Usuario, Cliente

from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# ==========================
# CONFIGURAÇÕES
# ==========================

SECRET_KEY = "PDV_STORE_MASTER_2026_CHAVE_SUPER_SECRETA"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_HOURS = 24

# ==========================
# SENHAS
# ==========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(
    senha: str,
    hash_salvo: str
):
    return pwd_context.verify(
        senha,
        hash_salvo
    )


# ==========================
# JWT
# ==========================

def criar_token(dados: dict):

    payload = dados.copy()

    expira = datetime.utcnow() + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )

    payload.update(
        {
            "exp": expira
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def validar_token(token: str):

    try:

        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return dados

    except Exception:

        return None


@router.get("/teste")
def teste():

    return {
        "status": "ok",
        "mensagem": "Auth funcionando."
    }


from pydantic import BaseModel


class LoginRequest(BaseModel):
    usuario: str
    senha: str


@router.post("/login")
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        print("=== LOGIN INICIADO ===")
        print("Usuário:", dados.usuario)

        usuario = db.query(Usuario).filter(
            Usuario.usuario == dados.usuario
        ).first()

        print("Consulta concluída")

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Usuário não encontrado."
            )

        print("Verificando senha")

        if not verificar_senha(
            dados.senha,
            usuario.senha_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Senha inválida."
            )

        print("Criando token")

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

    except Exception as e:
        print("ERRO LOGIN:", repr(e))
        raise


class AdminInicial(BaseModel):
    nome: str
    usuario: str
    email: str
    senha: str


@router.post("/criar-admin")
def criar_admin(
    dados: AdminInicial,
    db: Session = Depends(get_db)
):

    existe_usuario = db.query(Usuario).filter(
        Usuario.usuario == dados.usuario
    ).first()

    if existe_usuario:
        raise HTTPException(
            status_code=400,
            detail="Usuário já cadastrado."
        )

    existe_email = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if existe_email:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado."
        )

    cliente = Cliente(
        nome=dados.nome,
        empresa="Minha Empresa",
        email=dados.email,
        plano="ANUAL",
        status="ATIVO"
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    novo_usuario = Usuario(
        cliente_id=cliente.id,
        usuario=dados.usuario,
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash(dados.senha),
        perfil="ADMIN",
        ativo=True
    )

    db.add(novo_usuario)
    db.commit()

    return {
        "status": "ok",
        "mensagem": "Administrador criado com sucesso."
    }