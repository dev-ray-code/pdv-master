from datetime import datetime
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import Cliente, Licenca


class LicencaService:

    @staticmethod
    def gerar_chave():

        while True:

            chave = (
                "PDV-"
                + "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4))
                + "-"
                + "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4))
                + "-"
                + "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4))
            )

            return chave

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

                "empresa": cliente.empresa,

                "usuario": cliente.nome,

                "chave": licenca.chave,

                "plano": licenca.plano,

                "status": licenca.status,

                "validade": licenca.validade,

                "limite_computadores": licenca.limite_computadores,

                "criado_em": licenca.criado_em

            })

        return resultado

    @staticmethod
    def buscar(db: Session, licenca_id: int):

        licenca = (
            db.query(Licenca)
            .filter(Licenca.id == licenca_id)
            .first()
        )

        if not licenca:

            raise HTTPException(
                status_code=404,
                detail="Licença não encontrada."
            )

        return licenca

    @staticmethod
    def criar(db: Session, dados):

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

        chave = LicencaService.gerar_chave()

        while (
            db.query(Licenca)
            .filter(
                Licenca.chave == chave
            )
            .first()
        ):

            chave = LicencaService.gerar_chave()

        nova = Licenca(

            cliente_id=cliente.id,

            chave=chave,

            plano=dados.plano,

            status="ATIVA",

            validade=dados.validade,

            limite_computadores=dados.limite_computadores

        )

        db.add(nova)

        db.commit()

        db.refresh(nova)

        return {

            "empresa": cliente.empresa,

            "usuario": cliente.nome,

            "chave": nova.chave,

            "status": nova.status,

            "plano": nova.plano,

            "validade": nova.validade

        }

    @staticmethod
    def validar(db: Session, chave: str):

        licenca = (
            db.query(Licenca)
            .filter(Licenca.chave == chave)
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

        cliente = (
            db.query(Cliente)
            .filter(
                Cliente.id == licenca.cliente_id
            )
            .first()
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

            "limite_computadores": licenca.limite_computadores

        }

    @staticmethod
    def atualizar(db: Session, licenca_id: int, dados):

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

    @staticmethod
    def excluir(db: Session, licenca_id: int):

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

    