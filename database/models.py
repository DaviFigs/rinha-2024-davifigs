from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .connection import engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()