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
# LICENÇAS
# ==========================================================

class Licenca(Base):
    __tablename__ = "licencas"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    codigo = Column(
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

    data_ativacao = Column(
        DateTime,
        default=datetime.utcnow
    )

    data_vencimento = Column(DateTime)

    limite_computadores = Column(
        Integer,
        default=1
    )

    limite_usuarios = Column(
        Integer,
        default=5
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
# ATUALIZAÇÕES
# ==========================================================

class Atualizacao(Base):
    __tablename__ = "atualizacoes"

    id = Column(Integer, primary_key=True)

    versao = Column(String(30))

    descricao = Column(String(500))

    arquivo = Column(String(300))

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )


# ==========================================================
# CLIENTES
# ==========================================================

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)

    nome = Column(String(200))

    empresa = Column(String(200))

    telefone = Column(String(50))

    email = Column(String(200))

    cidade = Column(String(100))

    estado = Column(String(50))

    proprietario = Column(String(200))

    cnpj = Column(String(30))

    plano = Column(
        String(50),
        default="ANUAL"
    )

    status = Column(
        String(30),
        default="ATIVO"
    )

    validade = Column(Date)

    max_dispositivos = Column(
        Integer,
        default=1
    )

    max_usuarios = Column(
        Integer,
        default=5
    )

    token_api = Column(String(255))

    ultimo_acesso = Column(DateTime)

    atualizado_em = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    licencas = relationship(
        "Licenca",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    usuarios = relationship(
        "Usuario",
        cascade="all, delete-orphan"
    )

    dispositivos = relationship(
        "Dispositivo",
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
        ForeignKey("clientes.id")
    )

    licenca_id = Column(
        Integer,
        ForeignKey("licencas.id")
    )

    machine_id = Column(
        String(255),
        unique=True,
        nullable=False
    )

    nome_computador = Column(String(200))

    tipo = Column(String(30))          # WINDOWS / ANDROID / IOS

    sistema_operacional = Column(String(100))

    versao_pdv = Column(String(50))

    ip = Column(String(100))

    mac = Column(String(100))

    serial = Column(String(200))

    token = Column(String(255))

    status = Column(
        String(30),
        default="ATIVO"
    )

    primeira_ativacao = Column(
        DateTime,
        default=datetime.utcnow
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
        ForeignKey("clientes.id")
    )

    usuario = Column(
        String(100),
        unique=True
    )

    cliente = relationship("Cliente")

    nome = Column(String(200))

    email = Column(
        String(200),
        unique=True
    )

    senha_hash = Column(String(255))

    perfil = Column(
        String(50),
        default="OPERADOR"
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


# ==========================================================
# LOGS
# ==========================================================

class LogSistema(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )

    acao = Column(String(255))

    ip = Column(String(100))

    detalhes = Column(String(1000))

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )