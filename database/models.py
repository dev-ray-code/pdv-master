from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import declarative_base, relationship

from datetime import datetime, date


Base = declarative_base()


class Licenca(Base):
    __tablename__ = "licencas"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="licencas")

    empresa = Column(String(200))
    administrador = Column(String(200))

    chave = Column(String(120), unique=True)

    status = Column(String(30), default="ATIVA")

    validade = Column(DateTime)

    versao = Column(String(30))

    plano = Column(String(30), default="ANUAL")

    computadores = Column(Integer, default=1)

    ip = Column(String(100))

    maquina = Column(String(200))

    ativa = Column(Boolean, default=True)

    criado_em = Column(DateTime, default=datetime.utcnow)

    ultimo_acesso = Column(DateTime)

    cliente = relationship(
        "Cliente",
        back_populates="licencas"
    )


class Atualizacao(Base):
    __tablename__ = "atualizacoes"

    id = Column(Integer, primary_key=True)

    versao = Column(String(30))

    descricao = Column(String(500))

    arquivo = Column(String(300))

    criado_em = Column(DateTime, default=datetime.utcnow)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)

    nome = Column(String(200))
    empresa = Column(String(200))
    telefone = Column(String(50))
    email = Column(String(200))
    cidade = Column(String(100))
    estado = Column(String(50))

    criado_em = Column(DateTime, default=datetime.utcnow)

    licencas = relationship(
        "Licenca",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )