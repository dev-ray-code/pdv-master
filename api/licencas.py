from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import random
import string

from database.db import get_db
from database.models import Licenca, Cliente

router = APIRouter(
    prefix="/licencas",
    tags=["Licenças"]
)


def gerar_chave(db):

    caracteres = string.ascii_uppercase + string.digits

    while True:

        chave = "PDV-" + "-".join(
            "".join(random.choice(caracteres) for _ in range(4))
            for _ in range(3)
        )

        existe = db.query(Licenca).filter(
            Licenca.chave == chave
        ).first()

        if not existe:
            return chave


@router.post("/criar")
def criar_licenca(
    cliente_id: int,
    plano: str = "ANUAL",
    computadores: int = 1,
    validade: str = None,
    db: Session = Depends(get_db)
):

    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        return {
            "status": "Cliente não encontrado"
        }

    codigo = gerar_chave(db)

    data_validade = (
        datetime.strptime(validade, "%Y-%m-%d")
        if validade
        else datetime(2099, 12, 31)
    )

    licenca = Licenca(

        cliente_id=cliente.id,
        empresa=cliente.empresa,
        administrador=cliente.nome,

        chave=codigo,
        plano=plano.upper(),
        computadores=computadores,

        status="ATIVA",
        validade=data_validade,

        versao="1.0",
        ativa=True

    )

    db.add(licenca)
    db.commit()
    db.refresh(licenca)

    return {
        "status": "Licença criada",
        "codigo": codigo,
        "cliente": cliente.empresa
    }


@router.get("/validar/{codigo}")
def validar(codigo: str, db: Session = Depends(get_db)):

    licenca = db.query(Licenca).filter(
        Licenca.chave == codigo
    ).first()

    if not licenca:
        return {
            "valida": False,
            "motivo": "Licença inexistente"
        }

    agora = datetime.now()

    if not licenca.ativa:
        return {
            "valida": False,
            "motivo": "Licença bloqueada"
        }

    if licenca.validade and licenca.validade < agora:
        licenca.ativa = False
        licenca.status = "VENCIDA"
        db.commit()

        return {
            "valida": False,
            "motivo": "Licença vencida"
        }

    licenca.ultimo_acesso = agora
    db.commit()

    return {
        "valida": True,
        "cliente": licenca.empresa,
        "status": licenca.status,
        "validade": licenca.validade.strftime("%Y-%m-%d"),
        "plano": licenca.plano
    }

from fastapi import Body

@router.post("/login")
def login_licenca(
    administrador: str = Body(...),
    chave: str = Body(...),
    hardware_id: str = Body(None),
    db: Session = Depends(get_db)
):
    licenca = db.query(Licenca).filter(
        Licenca.administrador == administrador,
        Licenca.chave == chave
    ).first()

    if not licenca:
        return {
            "ok": False,
            "mensagem": "Usuário ou senha inválidos."
        }

    agora = datetime.now()

    if hardware_id:
        if not licenca.maquina:
            licenca.maquina = hardware_id

        elif licenca.maquina != hardware_id:
            return {
                "ok": False,
                "mensagem": "Esta licença já está sendo utilizada em outro computador."
            }

    if not licenca.ativa:
        return {
            "ok": False,
            "mensagem": "Licença bloqueada."
        }

    if licenca.validade and licenca.validade < agora:
        return {
            "ok": False,
            "mensagem": "Licença vencida."
        }

    licenca.ultimo_acesso = agora
    db.commit()

    return {
        "ok": True,
        "id": licenca.id,
        "cliente_id": licenca.cliente_id,
        "empresa": licenca.empresa,
        "administrador": licenca.administrador,
        "plano": licenca.plano,
        "status": licenca.status,
        "validade": licenca.validade.strftime("%Y-%m-%d") if licenca.validade else None
    }

@router.post("/bloquear/{codigo}")
def bloquear(codigo: str, db: Session = Depends(get_db)):

    licenca = db.query(Licenca).filter(
        Licenca.chave == codigo
    ).first()

    if not licenca:
        return {
            "status": "Licença não encontrada"
        }

    licenca.ativa = False
    licenca.status = "BLOQUEADA"

    db.commit()

    return {
        "status": "Licença bloqueada"
    }

@router.post("/desbloquear/{codigo}")
def desbloquear(codigo: str, db: Session = Depends(get_db)):

    licenca = db.query(Licenca).filter(
        Licenca.chave == codigo
    ).first()

    if not licenca:
        return {
            "status": "Licença não encontrada"
        }

    licenca.ativa = True
    licenca.status = "ATIVA"

    db.commit()

    return {
        "status": "Licença desbloqueada"
    }


@router.get("/listar")
def listar_licencas(db: Session = Depends(get_db)):

    licencas = db.query(Licenca).all()

    return [
        {
            "id": l.id,
            "cliente_id": l.cliente_id,
            "empresa": l.empresa,
            "administrador": l.administrador,
            "chave": l.chave,
            "plano": l.plano,
            "computadores": l.computadores,
            "status": l.status,
            "validade": l.validade.strftime("%d/%m/%Y") if l.validade else "",
            "versao": l.versao,
            "ativa": l.ativa
        }
        for l in licencas
    ]


@router.delete("/excluir/{codigo}")
def excluir_licenca(codigo: str, db: Session = Depends(get_db)):

    licenca = db.query(Licenca).filter(
        Licenca.chave == codigo
    ).first()

    if not licenca:
        return {
            "status": "Licença não encontrada"
        }

    db.delete(licenca)
    db.commit()

    return {
        "status": "Licença excluída"
    }

@router.post("/clientes/criar")
def criar_cliente(
    nome: str,
    empresa: str,
    telefone: str,
    email: str,
    cidade: str,
    estado: str,
    db: Session = Depends(get_db)
):

    cliente = Cliente(
        nome=nome,
        empresa=empresa,
        telefone=telefone,
        email=email,
        cidade=cidade,
        estado=estado
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return {
        "status": "Cliente cadastrado",
        "id": cliente.id
    }


@router.get("/clientes/listar")
def listar_clientes(db: Session = Depends(get_db)):

    clientes = db.query(Cliente).order_by(Cliente.empresa).all()

    return [
        {
            "id": c.id,
            "nome": c.nome,
            "empresa": c.empresa,
            "telefone": c.telefone,
            "email": c.email,
            "cidade": c.cidade,
            "estado": c.estado
        }
        for c in clientes
    ]


@router.delete("/clientes/excluir/{id}")
def excluir_cliente(id: int, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(
        Cliente.id == id
    ).first()

    if not cliente:
        return {
            "status": "Cliente não encontrado"
        }

    db.delete(cliente)
    db.commit()

    return {
        "status": "Cliente excluído"
    }

@router.post("/renovar/{codigo}")
def renovar_licenca(
    codigo: str,
    validade: str,
    db: Session = Depends(get_db)
):

    licenca = db.query(Licenca).filter(
        Licenca.chave == codigo
    ).first()

    if not licenca:
        return {
            "status": "Licença não encontrada"
        }

    licenca.validade = datetime.strptime(
        validade,
        "%Y-%m-%d"
    )

    licenca.status = "ATIVA"
    licenca.ativa = True

    db.commit()

    return {
        "status": "Licença renovada"
    }

@router.post("/ativar")
def ativar_licenca(
    codigo: str,
    cliente: str,
    db: Session = Depends(get_db)
):
    licenca = db.query(Licenca).filter(
        Licenca.chave == codigo
    ).first()

    if not licenca:
        return {
            "status": "erro",
            "mensagem": "Licença inexistente"
        }

    if not licenca.ativa:
        return {
            "status": "erro",
            "mensagem": "Licença bloqueada"
        }

    return {
        "status": "ok",
        "codigo": licenca.chave,
        "empresa": licenca.empresa,
        "administrador": licenca.administrador,
        "validade": licenca.validade.strftime("%Y-%m-%d")
    }