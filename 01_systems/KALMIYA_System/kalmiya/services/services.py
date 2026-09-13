from sqlalchemy.orm import Session
from kalmiya.models import models
from kalmiya.repositories.repositories import (
    UsuarioRepository, ConversacionRepository, 
    MensajeRepository, MemoriaRepository
)

class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, item_id: int):
        usuario = self.repo.get_by_id(item_id)
        if not usuario:
            raise ValueError(f"Usuario con ID {item_id} no encontrado")
        return usuario

    def create_usuario(self, data: dict):
        if self.repo.get_by_username(data.get('username')):
            raise ValueError(f"Ya existe un usuario con username: {data.get('username')}")
        if self.repo.get_by_email(data.get('email')):
            raise ValueError(f"Ya existe un usuario con email: {data.get('email')}")
        return self.repo.save(models.Usuario(**data))

    def update_usuario(self, item_id: int, data: dict):
        usuario = self.get_by_id(item_id)
        for key, value in data.items():
            setattr(usuario, key, value)
        return self.repo.save(usuario)

    def delete_usuario(self, item_id: int):
        usuario = self.get_by_id(item_id)
        self.repo.delete(usuario)
        return True

class ConversacionService:
    def __init__(self, db: Session):
        self.repo = ConversacionRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, item_id: int):
        conversacion = self.repo.get_by_id(item_id)
        if not conversacion:
            raise ValueError(f"Conversacion con ID {item_id} no encontrada")
        return conversacion

    def create_conversacion(self, data: dict):
        if not self.usuario_repo.get_by_id(data.get('usuario_id')):
            raise ValueError(f"Usuario con ID {data.get('usuario_id')} no existe")
        return self.repo.save(models.Conversacion(**data))

    def update_conversacion(self, item_id: int, data: dict):
        conversacion = self.get_by_id(item_id)
        for key, value in data.items():
            setattr(conversacion, key, value)
        return self.repo.save(conversacion)

    def delete_conversacion(self, item_id: int):
        conversacion = self.get_by_id(item_id)
        self.repo.delete(conversacion)
        return True

class MensajeService:
    def __init__(self, db: Session):
        self.repo = MensajeRepository(db)
        self.conversacion_repo = ConversacionRepository(db)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, item_id: int):
        mensaje = self.repo.get_by_id(item_id)
        if not mensaje:
            raise ValueError(f"Mensaje con ID {item_id} no encontrado")
        return mensaje

    def get_by_conversacion(self, conversacion_id: int):
        return self.repo.get_by_conversacion_id(conversacion_id)

    def create_mensaje(self, data: dict):
        if not self.conversacion_repo.get_by_id(data.get('conversacion_id')):
            raise ValueError(f"Conversacion con ID {data.get('conversacion_id')} no existe")
        if data.get('rol') not in ['user', 'assistant', 'system']:
            raise ValueError("El rol debe ser 'user', 'assistant' o 'system'")
        return self.repo.save(models.Mensaje(**data))

    def update_mensaje(self, item_id: int, data: dict):
        mensaje = self.get_by_id(item_id)
        for key, value in data.items():
            setattr(mensaje, key, value)
        return self.repo.save(mensaje)

    def delete_mensaje(self, item_id: int):
        mensaje = self.get_by_id(item_id)
        self.repo.delete(mensaje)
        return True

class MemoriaService:
    def __init__(self, db: Session):
        self.repo = MemoriaRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, item_id: int):
        memoria = self.repo.get_by_id(item_id)
        if not memoria:
            raise ValueError(f"Memoria con ID {item_id} no encontrada")
        return memoria

    def create_memoria(self, data: dict):
        if not self.usuario_repo.get_by_id(data.get('usuario_id')):
            raise ValueError(f"Usuario con ID {data.get('usuario_id')} no existe")
        return self.repo.save(models.Memoria(**data))

    def update_memoria(self, item_id: int, data: dict):
        memoria = self.get_by_id(item_id)
        for key, value in data.items():
            setattr(memoria, key, value)
        return self.repo.save(memoria)

    def delete_memoria(self, item_id: int):
        memoria = self.get_by_id(item_id)
        self.repo.delete(memoria)
        return True
