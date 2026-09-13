from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from kalmiya.database import get_db
from kalmiya.services.services import (
    UsuarioService, ConversacionService,
    MensajeService, MemoriaService
)

router = APIRouter()

# =======================
# USUARIOS
# =======================
@router.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    return UsuarioService(db).get_all()

@router.get("/usuarios/{item_id}")
def get_usuario(item_id: int, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).get_by_id(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/usuarios")
def create_usuario(data: dict, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).create_usuario(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/usuarios/{item_id}")
def update_usuario(item_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).update_usuario(item_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/usuarios/{item_id}")
def delete_usuario(item_id: int, db: Session = Depends(get_db)):
    try:
        UsuarioService(db).delete_usuario(item_id)
        return {"message": "Usuario eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =======================
# CONVERSACIONES
# =======================
@router.get("/conversaciones")
def get_conversaciones(db: Session = Depends(get_db)):
    return ConversacionService(db).get_all()

@router.get("/conversaciones/{item_id}")
def get_conversacion(item_id: int, db: Session = Depends(get_db)):
    try:
        return ConversacionService(db).get_by_id(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/conversaciones")
def create_conversacion(data: dict, db: Session = Depends(get_db)):
    try:
        return ConversacionService(db).create_conversacion(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/conversaciones/{item_id}")
def update_conversacion(item_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        return ConversacionService(db).update_conversacion(item_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/conversaciones/{item_id}")
def delete_conversacion(item_id: int, db: Session = Depends(get_db)):
    try:
        ConversacionService(db).delete_conversacion(item_id)
        return {"message": "Conversacion eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =======================
# MENSAJES
# =======================
@router.get("/mensajes")
def get_mensajes(conversacion_id: int = None, db: Session = Depends(get_db)):
    service = MensajeService(db)
    if conversacion_id:
        return service.get_by_conversacion(conversacion_id)
    return service.get_all()

@router.get("/mensajes/{item_id}")
def get_mensaje(item_id: int, db: Session = Depends(get_db)):
    try:
        return MensajeService(db).get_by_id(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/mensajes")
def create_mensaje(data: dict, db: Session = Depends(get_db)):
    try:
        return MensajeService(db).create_mensaje(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/mensajes/{item_id}")
def update_mensaje(item_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        return MensajeService(db).update_mensaje(item_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/mensajes/{item_id}")
def delete_mensaje(item_id: int, db: Session = Depends(get_db)):
    try:
        MensajeService(db).delete_mensaje(item_id)
        return {"message": "Mensaje eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =======================
# MEMORIAS
# =======================
@router.get("/memorias")
def get_memorias(db: Session = Depends(get_db)):
    return MemoriaService(db).get_all()

@router.get("/memorias/{item_id}")
def get_memoria(item_id: int, db: Session = Depends(get_db)):
    try:
        return MemoriaService(db).get_by_id(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/memorias")
def create_memoria(data: dict, db: Session = Depends(get_db)):
    try:
        return MemoriaService(db).create_memoria(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/memorias/{item_id}")
def update_memoria(item_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        return MemoriaService(db).update_memoria(item_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/memorias/{item_id}")
def delete_memoria(item_id: int, db: Session = Depends(get_db)):
    try:
        MemoriaService(db).delete_memoria(item_id)
        return {"message": "Memoria eliminada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
