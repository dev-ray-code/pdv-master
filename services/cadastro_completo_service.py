import secrets
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import (
    Cliente,
    Licenca,
    Usuario
)

from services.auth_service import gerar_hash
from services.licenca_service import LicencaService


class CadastroCompletoService:

    # ======================================================
    # GERAR USUÁRIO
    # ======================================================

    @staticmethod
    def gerar_usuario(db: Session, empresa: str):

        # Remove espaços e caracteres desnecessários
        base = "".join(
            caractere
            for caractere in empresa.lower()
            if caractere.isalnum()
        )

        if not base:
            base = "cliente"

        base = base[:20]

        while True:

            numero = secrets.token_hex(3)

            usuario = f"{base}_{numero}"

            existe = (
                db.query(Usuario)
                .filter(
                    Usuario.usuario == usuario
                )
                .first()
            )

            if not existe:
                return usuario

    # ======================================================
    # GERAR SENHA
    # ======================================================

    @staticmethod
    def gerar_senha():

        caracteres = (
            string.ascii_letters
            + string.digits
        )

        return "".join(
            secrets.choice(caracteres)
            for _ in range(10)
        )

    # ======================================================
    # CADASTRO COMPLETO
    # ======================================================

    @staticmethod
    def criar(
        db: Session,
        dados
    ):

        try:

            # ==================================================
            # 1. CRIAR CLIENTE
            # ==================================================

            cliente = Cliente(

                empresa=dados.empresa,

                nome=dados.nome,

                telefone=dados.telefone,

                endereco=dados.endereco

            )

            db.add(cliente)

            db.flush()

            # ==================================================
            # 2. GERAR CHAVE DA LICENÇA
            # ==================================================

            chave = LicencaService.gerar_chave()

            while (
                db.query(Licenca)
                .filter(
                    Licenca.chave == chave
                )
                .first()
            ):

                chave = LicencaService.gerar_chave()

            # ==================================================
            # 3. CRIAR LICENÇA
            # ==================================================

            licenca = Licenca(

                cliente_id=cliente.id,

                chave=chave,

                plano=dados.plano,

                status="ATIVA",

                validade=dados.validade,

                limite_computadores=
                    dados.limite_computadores

            )

            db.add(licenca)

            db.flush()

            # ==================================================
            # 4. GERAR LOGIN
            # ==================================================

            usuario_login = (
                CadastroCompletoService.gerar_usuario(
                    db,
                    dados.empresa
                )
            )

            # ==================================================
            # 5. GERAR SENHA
            # ==================================================

            senha = (
                CadastroCompletoService.gerar_senha()
            )

            # ==================================================
            # 6. CRIAR USUÁRIO
            # ==================================================

            usuario = Usuario(

                cliente_id=cliente.id,

                usuario=usuario_login,

                senha_hash=gerar_hash(senha),

                perfil="ADMIN",

                ativo=True

            )

            db.add(usuario)

            # ==================================================
            # 7. SALVAR TUDO
            # ==================================================

            db.commit()

            db.refresh(cliente)
            db.refresh(licenca)
            db.refresh(usuario)

            # ==================================================
            # 8. RETORNAR CREDENCIAIS
            # ==================================================

            return {

                "cliente_id": cliente.id,

                "empresa": cliente.empresa,

                "nome": cliente.nome,

                "usuario": usuario.usuario,

                "senha": senha,

                "licenca_id": licenca.id,

                "chave": licenca.chave,

                "plano": licenca.plano,

                "status": licenca.status,

                "validade": licenca.validade,

                "limite_computadores":
                    licenca.limite_computadores

            }

        except Exception as erro:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar cadastro: {str(erro)}"
            )