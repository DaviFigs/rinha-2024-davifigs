from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    limite = Column(Integer, nullable=False)

class Transacao(Base):
    __tablename__ = "transacao"
    id = Column(Integer, primary_key=True, nullable=False)
    cliente_id =Column(Integer, ForeignKey("cliente.id"), nullable=False)
    valor = Column(Integer, nullable=False)
    tipo = Column(String(1), nullable=False)
    descricao = Column(String(10), nullable=False)
    cliente = relationship("Cliente",back_populates="transacao")

class Saldo(Base):
    __tablename__ = "saldo"
    id = Column(Integer, primary_key=True, nullable=False)
    cliente_id =Column(Integer, ForeignKey("cliente.id"), nullable=False)
    valor = Column(Integer, nullable=False)
    cliente = relationship("Cliente",back_populates="transacao")

