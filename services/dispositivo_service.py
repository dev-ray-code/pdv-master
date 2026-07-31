from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import (
    Cliente,
    Dispositivo,
    Licenca
)


class DispositivoService:

    @staticmethod
    def listar(db: Session):
        return db.query(Dispositivo).order_by(
            Dispositivo.id.desc()
        ).all()

    @staticmethod
    def buscar(db: Session, dispositivo_id: int):

        dispositivo = db.query(Dispositivo).filter(
            Dispositivo.id == dispositivo_id
        ).first()

        if not dispositivo:
            raise HTTPException(
                status_code=404,
                detail="Dispositivo não encontrado."
            )

        return dispositivo

    @staticmethod
    def conectar(db: Session, dados):

        licenca = db.query(Licenca).filter(
            Licenca.codigo == dados.codigo_licenca
        ).first()

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
            licenca.data_vencimento
            and
            licenca.data_vencimento < datetime.utcnow()
        ):
            raise HTTPException(
                status_code=403,
                detail="Licença expirada."
            )

        dispositivo = db.query(Dispositivo).filter(
            Dispositivo.machine_id == dados.machine_id
        ).first()

        if dispositivo:

            dispositivo.nome_computador = dados.nome_computador
            dispositivo.sistema_operacional = dados.sistema_operacional
            dispositivo.versao_pdv = dados.versao_pdv
            dispositivo.ip = dados.ip
            dispositivo.mac = dados.mac
            dispositivo.serial = dados.serial
            dispositivo.ultimo_acesso = datetime.utcnow()
            dispositivo.status = "ATIVO"

            db.commit()
            db.refresh(dispositivo)

            return {
                "status": "AUTORIZADO",
                "mensagem": "Dispositivo já cadastrado.",
                "cliente_id": licenca.cliente_id,
                "licenca_id": licenca.id
            }

        quantidade = db.query(Dispositivo).filter(
            Dispositivo.licenca_id == licenca.id,
            Dispositivo.status == "ATIVO"
        ).count()

        if quantidade >= licenca.limite_computadores:
            raise HTTPException(
                status_code=403,
                detail="Limite de computadores atingido."
            )

        novo = Dispositivo(
            cliente_id=licenca.cliente_id,
            licenca_id=licenca.id,
            machine_id=dados.machine_id,
            nome_computador=dados.nome_computador,
            tipo=dados.tipo,
            sistema_operacional=dados.sistema_operacional,
            versao_pdv=dados.versao_pdv,
            ip=dados.ip,
            mac=dados.mac,
            serial=dados.serial,
            status="ATIVO",
            primeira_ativacao=datetime.utcnow(),
            ultimo_acesso=datetime.utcnow()
        )

        db.add(novo)
        db.commit()
        db.refresh(novo)

        return {
            "status": "AUTORIZADO",
            "mensagem": "Dispositivo registrado com sucesso.",
            "cliente_id": licenca.cliente_id,
            "licenca_id": licenca.id
        }

    @staticmethod
    def bloquear(db: Session, dispositivo_id: int):

        dispositivo = DispositivoService.buscar(
            db,
            dispositivo_id
        )

        dispositivo.status = "BLOQUEADO"

        db.commit()

        return {
            "status": "ok",
            "mensagem": "Dispositivo bloqueado."
        }

    @staticmethod
    def desbloquear(db: Session, dispositivo_id: int):

        dispositivo = DispositivoService.buscar(
            db,
            dispositivo_id
        )

        dispositivo.status = "ATIVO"

        db.commit()

        return {
            "status": "ok",
            "mensagem": "Dispositivo desbloqueado."
        }

    @staticmethod
    def excluir(db: Session, dispositivo_id: int):

        dispositivo = DispositivoService.buscar(
            db,
            dispositivo_id
        )

        db.delete(dispositivo)
        db.commit()

        return {
            "status": "ok",
            "mensagem": "Dispositivo removido."
        }