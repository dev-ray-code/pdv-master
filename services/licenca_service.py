from datetime import datetime
import random
import secrets
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import Cliente, Licenca, Usuario
from services.auth_service import gerar_hash


class LicencaService:

    # ==========================================================
    # GERAR CHAVE DA LICENÇA
    # ==========================================================

    @staticmethod
    def gerar_chave():

        while True:

            chave = (
                "PDV-"
                + "".join(
                    random.choices(
                        "ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
                        k=4
                    )
                )
                + "-"
                + "".join(
                    random.choices(
                        "ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
                        k=4
                    )
                )
                + "-"
                + "".join(
                    random.choices(
                        "ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
                        k=4
                    )
                )
            )

            return chave

    # ==========================================================
    # GERAR USUÁRIO
    # ==========================================================

    @staticmethod
    def gerar_usuario(empresa: str):

        base = "".join(
            caractere.lower()
            for caractere in empresa
            if caractere.isalnum()
        )

        if not base:
            base = "cliente"

        base = base[:30]

        usuario = base
        contador = 1

        while True:

            existe = None

            # Essa função será usada dentro do criar(),
            # portanto a verificação final será feita lá.

            if existe is None:
                return usuario

            usuario = f"{base}{contador}"

            contador += 1

    # ==========================================================
    # GERAR SENHA
    # ==========================================================

    @staticmethod
    def gerar_senha():

        caracteres = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
        )

        return "".join(
            secrets.choice(caracteres)
            for _ in range(10)
        )

    # ==========================================================
    # LISTAR
    # ==========================================================

    @staticmethod
    def listar(db: Session):

        resultado = []

        licencas = (
            db.query(Licenca)
            .order_by(Licenca.id.desc())
            .all()
        )

        for licenca in licencas:

            cliente = (
                db.query(Cliente)
                .filter(
                    Cliente.id == licenca.cliente_id
                )
                .first()
            )

            resultado.append({

                "id": licenca.id,

                "cliente_id": licenca.cliente_id,

                "empresa": (
                    cliente.empresa
                    if cliente
                    else ""
                ),

                "usuario": (
                    cliente.nome
                    if cliente
                    else ""
                ),

                "chave": licenca.chave,

                "plano": licenca.plano,

                "status": licenca.status,

                "validade": licenca.validade,

                "limite_computadores":
                    licenca.limite_computadores,

                "criado_em": licenca.criado_em

            })

        return resultado

    # ==========================================================
    # BUSCAR
    # ==========================================================

    @staticmethod
    def buscar(
        db: Session,
        licenca_id: int
    ):

        licenca = (
            db.query(Licenca)
            .filter(
                Licenca.id == licenca_id
            )
            .first()
        )

        if not licenca:

            raise HTTPException(
                status_code=404,
                detail="Licença não encontrada."
            )

        return licenca

    # ==========================================================
    # CRIAR LICENÇA
    # ==========================================================

    @staticmethod
    def criar(
        db: Session,
        dados
    ):

        cliente = (
            db.query(Cliente)
            .filter(
                Cliente.id == dados.cliente_id
            )
            .first()
        )

        if not cliente:

            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )

        # ------------------------------------------------------
        # GERAR CHAVE ÚNICA
        # ------------------------------------------------------

        chave = LicencaService.gerar_chave()

        while (
            db.query(Licenca)
            .filter(
                Licenca.chave == chave
            )
            .first()
        ):

            chave = LicencaService.gerar_chave()

        # ------------------------------------------------------
        # CRIAR LICENÇA
        # ------------------------------------------------------

        nova = Licenca(

            cliente_id=cliente.id,

            chave=chave,

            plano=dados.plano,

            status="ATIVA",

            validade=dados.validade,

            limite_computadores=
                dados.limite_computadores

        )

        db.add(nova)

        db.flush()

        # ------------------------------------------------------
        # GERAR LOGIN
        # ------------------------------------------------------

        base_usuario = "".join(
            caractere.lower()
            for caractere in cliente.empresa
            if caractere.isalnum()
        )

        if not base_usuario:

            base_usuario = "cliente"

        base_usuario = base_usuario[:30]

        usuario_login = base_usuario

        contador = 1

        while (
            db.query(Usuario)
            .filter(
                Usuario.usuario == usuario_login
            )
            .first()
        ):

            usuario_login = (
                f"{base_usuario}{contador}"
            )

            contador += 1

        # ------------------------------------------------------
        # GERAR SENHA
        # ------------------------------------------------------

        senha = LicencaService.gerar_senha()

        # ------------------------------------------------------
        # CRIAR USUÁRIO DO CLIENTE
        # ------------------------------------------------------

        novo_usuario = Usuario(

            cliente_id=cliente.id,

            usuario=usuario_login,

            senha_hash=gerar_hash(senha),

            perfil="ADMIN",

            ativo=True

        )

        db.add(novo_usuario)

        db.commit()

        db.refresh(nova)

        db.refresh(novo_usuario)

        # ------------------------------------------------------
        # RETORNAR DADOS PARA O ADMINISTRADOR
        # ------------------------------------------------------

        return {

            "id": nova.id,

            "cliente_id": cliente.id,

            "empresa": cliente.empresa,

            "usuario": usuario_login,

            "senha": senha,

            "chave": nova.chave,

            "status": nova.status,

            "plano": nova.plano,

            "validade": nova.validade,

            "limite_computadores":
                nova.limite_computadores,

            "criado_em": nova.criado_em

        }

    # ==========================================================
    # VALIDAR LICENÇA
    # ==========================================================

    @staticmethod
    def validar(
        db: Session,
        chave: str
    ):

        licenca = (
            db.query(Licenca)
            .filter(
                Licenca.chave == chave
            )
            .first()
        )

        if not licenca:

            raise HTTPException(
                status_code=404,
                detail="Licença não encontrada."
            )

        if licenca.status != "ATIVA":

            raise HTTPException(
                status_code=403,
                detail="Licença bloqueada."
            )

        if (
            licenca.validade
            and
            licenca.validade < datetime.utcnow().date()
        ):

            raise HTTPException(
                status_code=403,
                detail="Licença vencida."
            )

        cliente = (
            db.query(Cliente)
            .filter(
                Cliente.id == licenca.cliente_id
            )
            .first()
        )

        if not cliente:

            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )

        return {

            "autorizado": True,

            "empresa": cliente.empresa,

            "usuario": cliente.nome,

            "cliente_id": cliente.id,

            "licenca_id": licenca.id,

            "chave": licenca.chave,

            "plano": licenca.plano,

            "validade": licenca.validade,

            "limite_computadores":
                licenca.limite_computadores

        }

    # ==========================================================
    # ATUALIZAR
    # ==========================================================

    @staticmethod
    def atualizar(
        db: Session,
        licenca_id: int,
        dados
    ):

        licenca = LicencaService.buscar(
            db,
            licenca_id
        )

        for campo, valor in dados.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                licenca,
                campo,
                valor
            )

        db.commit()

        db.refresh(licenca)

        return licenca

    # ==========================================================
    # EXCLUIR
    # ==========================================================

    @staticmethod
    def excluir(
        db: Session,
        licenca_id: int
    ):

        licenca = LicencaService.buscar(
            db,
            licenca_id
        )

        db.delete(licenca)

        db.commit()

        return {

            "status": "ok",

            "mensagem": "Licença removida."

        }