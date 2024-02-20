from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Clientes(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    limite = Column(Integer, nullable=False)
    transacoes = relationship("Transacoes", back_populates="clientes")
    saldos = relationship("Saldos", back_populates="clientes")

class Transacoes(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, nullable=False)
    cliente_id =Column(Integer, ForeignKey("clientes.id"), nullable=False)
    valor = Column(Integer, nullable=False)
    tipo = Column(String(1), nullable=False)
    descricao = Column(String(10), nullable=False)
    cliente = relationship("Clientes",back_populates="transacoes")

class Saldos(Base):
    __tablename__ = "saldos"
    id = Column(Integer, primary_key=True, nullable=False)
    cliente_id =Column(Integer, ForeignKey("clientes.id"), nullable=False)
    valor = Column(Integer, nullable=False)
    cliente = relationship("Clientes",back_populates="saldos")



