from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
# pyrefly: ignore [missing-import]
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    conversaciones = relationship("Conversacion", back_populates="usuario", cascade="all, delete-orphan")
    memorias = relationship("Memoria", back_populates="usuario", cascade="all, delete-orphan")

class Conversacion(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="Activa")
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="conversaciones")
    mensajes = relationship("Mensaje", back_populates="conversacion", cascade="all, delete-orphan")

class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    rol = Column(String, nullable=False) # 'user' o 'assistant'
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    conversacion_id = Column(Integer, ForeignKey("conversaciones.id"), nullable=False)
    conversacion = relationship("Conversacion", back_populates="mensajes")

class Memoria(Base):
    __tablename__ = "memorias"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String, index=True, nullable=False)
    valor = Column(Text, nullable=False)
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="memorias")
