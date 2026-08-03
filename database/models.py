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
from datetime import datetime

Base = declarative_base()


# ==========================================================
# CLIENTES
# ==========================================================

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)

    empresa = Column(String(200), nullable=False)

    nome = Column(String(200), nullable=False)

    telefone = Column(String(50))

    endereco = Column(String(300))

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    licencas = relationship(
        "Licenca",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    dispositivos = relationship(
        "Dispositivo",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )


# ==========================================================
# LICENÇAS
# ==========================================================

class Licenca(Base):
    __tablename__ = "licencas"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    chave = Column(
        String(120),
        unique=True,
        nullable=False
    )

    plano = Column(
        String(30),
        default="ANUAL"
    )

    status = Column(
        String(30),
        default="ATIVA"
    )

    validade = Column(Date)

    limite_computadores = Column(
        Integer,
        default=1
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    cliente = relationship(
        "Cliente",
        back_populates="licencas"
    )

    dispositivos = relationship(
        "Dispositivo",
        back_populates="licenca",
        cascade="all, delete-orphan"
    )


# ==========================================================
# DISPOSITIVOS
# ==========================================================

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    licenca_id = Column(
        Integer,
        ForeignKey("licencas.id"),
        nullable=False
    )

    machine_id = Column(
        String(255),
        unique=True,
        nullable=False
    )

    nome_computador = Column(String(200))

    tipo = Column(String(30))

    sistema_operacional = Column(String(100))

    versao_pdv = Column(String(50))

    status = Column(
        String(30),
        default="ATIVO"
    )

    ultimo_acesso = Column(
        DateTime,
        default=datetime.utcnow
    )

    cliente = relationship(
        "Cliente",
        back_populates="dispositivos"
    )

    licenca = relationship(
        "Licenca",
        back_populates="dispositivos"
    )


# ==========================================================
# USUÁRIOS
# ==========================================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    usuario = Column(
        String(100),
        unique=True,
        nullable=False
    )

    senha_hash = Column(
        String(255),
        nullable=False
    )

    perfil = Column(
        String(50),
        default="ADMIN"
    )

    ativo = Column(
        Boolean,
        default=True
    )

    ultimo_login = Column(DateTime)

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )