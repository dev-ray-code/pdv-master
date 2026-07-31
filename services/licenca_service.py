from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import secrets

from database.models import Licenca, Cliente


class LicencaService:

    @staticmethod
    def gerar_codigo():
        return secrets.token_hex(16).upper()

    @staticmethod
    def listar(db: Session):
        return db.query(Licenca).order_by(Licenca.id.desc()).all()

    @staticmethod
    def buscar(db: Session, licenca_id: int):

        licenca = db.query(Licenca).filter(
            Licenca.id == licenca_id
        ).first()

        if not licenca:
            raise HTTPException(
                status_code=404,
                detail="Licença não encontrada."
            )

        return licenca

    @staticmethod
    def criar(db: Session, dados):

        cliente = db.query(Cliente).filter(
            Cliente.id == dados.cliente_id
        ).first()

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado."
            )

        codigo = LicencaService.gerar_codigo()

        while db.query(Licenca).filter(
            Licenca.codigo == codigo
        ).first():
            codigo = LicencaService.gerar_codigo()

        licenca = Licenca(
            cliente_id=dados.cliente_id,
            codigo=codigo,
            plano=dados.plano,
            status=dados.status,
            limite_computadores=dados.limite_computadores,
            limite_usuarios=dados.limite_usuarios,
            data_ativacao=dados.data_ativacao or datetime.utcnow(),
            data_vencimento=dados.data_vencimento
        )

        db.add(licenca)
        db.commit()
        db.refresh(licenca)

        return licenca

    @staticmethod
    def validar(db: Session, codigo: str):

        licenca = db.query(Licenca).filter(
            Licenca.codigo == codigo
        ).first()

        if not licenca:
            raise HTTPException(
                status_code=404,
                detail="Licença não encontrada."
            )

        if licenca.status != "ATIVO":
            raise HTTPException(
                status_code=403,
                detail="Licença bloqueada."
            )

        if (
            licenca.data_vencimento
            and licenca.data_vencimento < datetime.utcnow()
        ):
            raise HTTPException(
                status_code=403,
                detail="Licença vencida."
            )

        cliente = db.query(Cliente).filter(
            Cliente.id == licenca.cliente_id
        ).first()

        return {
            "valido": True,
            "cliente_id": cliente.id,
            "empresa": cliente.empresa,
            "plano": licenca.plano,
            "status": licenca.status,
            "codigo": licenca.codigo,
            "limite_computadores": licenca.limite_computadores,
            "limite_usuarios": licenca.limite_usuarios
        }

    @staticmethod
    def atualizar(db: Session, licenca_id: int, dados):

        licenca = LicencaService.buscar(db, licenca_id)

        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(licenca, campo, valor)

        db.commit()
        db.refresh(licenca)

        return licenca

    @staticmethod
    def excluir(db: Session, licenca_id: int):

        licenca = LicencaService.buscar(db, licenca_id)

        db.delete(licenca)
        db.commit()

        return {
            "status": "ok",
            "mensagem": "Licença removida com sucesso."
        }