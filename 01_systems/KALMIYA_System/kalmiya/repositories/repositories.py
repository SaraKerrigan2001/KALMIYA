from sqlalchemy.orm import Session
from kalmiya.models import models

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Usuario).all()

    def get_by_id(self, usuario_id: int):
        return self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    def get_by_username(self, username: str):
        return self.db.query(models.Usuario).filter(models.Usuario.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(models.Usuario).filter(models.Usuario.email == email).first()

    def save(self, usuario: models.Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: models.Usuario):
        self.db.delete(usuario)
        self.db.commit()

class ConversacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Conversacion).all()

    def get_by_id(self, conversacion_id: int):
        return self.db.query(models.Conversacion).filter(models.Conversacion.id == conversacion_id).first()

    def get_by_usuario_id(self, usuario_id: int):
        return self.db.query(models.Conversacion).filter(models.Conversacion.usuario_id == usuario_id).all()

    def save(self, conversacion: models.Conversacion):
        self.db.add(conversacion)
        self.db.commit()
        self.db.refresh(conversacion)
        return conversacion

    def delete(self, conversacion: models.Conversacion):
        self.db.delete(conversacion)
        self.db.commit()

class MensajeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Mensaje).all()

    def get_by_id(self, mensaje_id: int):
        return self.db.query(models.Mensaje).filter(models.Mensaje.id == mensaje_id).first()

    def get_by_conversacion_id(self, conversacion_id: int):
        return self.db.query(models.Mensaje).filter(models.Mensaje.conversacion_id == conversacion_id).order_by(models.Mensaje.fecha.asc()).all()

    def save(self, mensaje: models.Mensaje):
        self.db.add(mensaje)
        self.db.commit()
        self.db.refresh(mensaje)
        return mensaje

    def delete(self, mensaje: models.Mensaje):
        self.db.delete(mensaje)
        self.db.commit()

class MemoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Memoria).all()

    def get_by_id(self, memoria_id: int):
        return self.db.query(models.Memoria).filter(models.Memoria.id == memoria_id).first()

    def get_by_usuario_id(self, usuario_id: int):
        return self.db.query(models.Memoria).filter(models.Memoria.usuario_id == usuario_id).all()

    def save(self, memoria: models.Memoria):
        self.db.add(memoria)
        self.db.commit()
        self.db.refresh(memoria)
        return memoria

    def delete(self, memoria: models.Memoria):
        self.db.delete(memoria)
        self.db.commit()
