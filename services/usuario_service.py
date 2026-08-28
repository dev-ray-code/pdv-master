from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models import Usuario
from services.auth_service import gerar_hash


class UsuarioService:

    @staticmethod
    def listar(db: Session):
        return db.query(Usuario).order_by(
            Usuario.id.desc()
        ).all()

    @staticmethod
    def buscar(
        db: Session,
        usuario_id: int
    ):

        usuario = db.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        return usuario

    @staticmethod
    def criar(
        db: Session,
        dados
    ):

        # ==================================================
        # VERIFICAR SE O USUÁRIO JÁ EXISTE
        # ==================================================

        existe = db.query(Usuario).filter(
            Usuario.usuario == dados.usuario
        ).first()

        if existe:
            raise HTTPException(
                status_code=400,
                detail="Usuário já existe."
            )

        # ==================================================
        # CRIAR USUÁRIO
        # ==================================================

        usuario = Usuario(

            cliente_id=dados.cliente_id,

            usuario=dados.usuario,

            senha_hash=gerar_hash(
                dados.senha
            ),

            perfil=dados.perfil,

            ativo=dados.ativo

        )

        db.add(usuario)

        db.commit()

        db.refresh(usuario)

        return usuario

    @staticmethod
    def atualizar(
        db: Session,
        usuario_id: int,
        dados
    ):

        usuario = UsuarioService.buscar(
            db,
            usuario_id
        )

        # ==================================================
        # ATUALIZAR USUÁRIO
        # ==================================================

        if dados.usuario is not None:

            existe = db.query(Usuario).filter(
                Usuario.usuario == dados.usuario,
                Usuario.id != usuario_id
            ).first()

            if existe:

                raise HTTPException(
                    status_code=400,
                    detail="Usuário já existe."
                )

            usuario.usuario = dados.usuario

        # ==================================================
        # ATUALIZAR PERFIL
        # ==================================================

        if dados.perfil is not None:

            usuario.perfil = dados.perfil

        # ==================================================
        # ATIVAR / DESATIVAR
        # ==================================================

        if dados.ativo is not None:

            usuario.ativo = dados.ativo

        # ==================================================
        # ALTERAR SENHA
        # ==================================================

        if dados.senha:

            usuario.senha_hash = gerar_hash(
                dados.senha
            )

        db.commit()

        db.refresh(usuario)

        return usuario

    @staticmethod
    def excluir(
        db: Session,
        usuario_id: int
    ):

        usuario = UsuarioService.buscar(
            db,
            usuario_id
        )

        db.delete(usuario)

        db.commit()

        return {

            "status": "ok",

            "mensagem": "Usuário removido."

        }