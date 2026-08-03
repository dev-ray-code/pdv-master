from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models import Cliente


class ClienteService:

    @staticmethod
    def listar(db: Session):
        return db.query(Cliente).order_by(
            Cliente.id.desc()
        ).all()

    @staticmethod
    def buscar(db: Session, cliente_id: int):

        cliente = db.query(Cliente).filter(
            Cliente.id == cliente_id
        ).first()

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )

        return cliente

    @staticmethod
    def criar(db: Session, dados):

        cliente = Cliente(
            empresa=dados.empresa,
            nome=dados.nome,
            telefone=dados.telefone,
            endereco=dados.endereco
        )

        db.add(cliente)
        db.commit()
        db.refresh(cliente)

        return cliente

    @staticmethod
    def atualizar(
        db: Session,
        cliente_id: int,
        dados
    ):

        cliente = ClienteService.buscar(
            db,
            cliente_id
        )

        for campo, valor in dados.model_dump(
            exclude_unset=True
        ).items():
            setattr(cliente, campo, valor)

        db.commit()
        db.refresh(cliente)

        return cliente

    @staticmethod
    def excluir(
        db: Session,
        cliente_id: int
    ):

        cliente = ClienteService.buscar(
            db,
            cliente_id
        )

        db.delete(cliente)
        db.commit()

        return {
            "status": "ok",
            "mensagem": "Cliente removido com sucesso."
        }