from sqlalchemy import (
    Column, Integer, String, Date, Numeric,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Posto(Base):
    __tablename__ = "postos"

    id_posto = Column(Integer, primary_key=True)
    cnpj = Column(String(18), nullable=False, unique=True)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))
    bandeira = Column(String(50))
    endereco = Column(String(255), nullable=False)
    numero = Column(String(20))
    bairro = Column(String(100))
    cep = Column(String(10))
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    regiao = Column(String(20))

    precos = relationship("Preco", back_populates="posto")


class Combustivel(Base):
    __tablename__ = "combustiveis"

    id_combustivel = Column(Integer, primary_key=True)
    descricao = Column(String(50), nullable=False, unique=True)
    unidade_medida = Column(String(10), nullable=False)

    precos = relationship("Preco", back_populates="combustivel")


class Preco(Base):
    __tablename__ = "precos"

    id_preco = Column(Integer, primary_key=True)
    id_posto = Column(Integer, ForeignKey("postos.id_posto"), nullable=False)
    id_combustivel = Column(Integer, ForeignKey("combustiveis.id_combustivel"), nullable=False)
    data_coleta = Column(Date, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    moeda = Column(String(2), default="R$")

    posto = relationship("Posto", back_populates="precos")
    combustivel = relationship("Combustivel", back_populates="precos")

    __table_args__ = (
        UniqueConstraint(
            "id_posto", "id_combustivel", "data_coleta",
            name="uq_preco_posto_comb_data"
        ),
    )
