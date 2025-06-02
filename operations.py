from typing import List, Optional
from sqlmodel import Session, select
from models import Progreso, CausaAbandono
import os
import shutil
from pathlib import Path
from fastapi import UploadFile

UPLOADS_DIR = "static/uploads"
Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)

async def save_image_file(image: UploadFile) -> str:
    if not image or not image.filename:
        return None

    safe_filename = Path(image.filename).name
    destination_path = os.path.join(UPLOADS_DIR, safe_filename)

    try:
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        print(f"Archivo guardado en: {destination_path}")
        return f"/uploads/{safe_filename}"
    except Exception as e:
        print(f"ERROR al guardar el archivo: {e}")
        return None


def delete_image_file(image_path: str):
    if image_path:
        file_to_delete = os.path.join("static", image_path.lstrip('/'))
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
            print(f"Imagen eliminada: {file_to_delete}")
        else:
            print(f"Advertencia: La imagen {file_to_delete} no se encontró en el disco para eliminar.")

def guardar_progreso(db: Session, progreso_data: Progreso) -> Progreso:
    db.add(progreso_data)
    db.commit()
    db.refresh(progreso_data)
    return progreso_data

def listar_progresos(db: Session, incluir_inactivos: bool = False) -> List[Progreso]:
    if incluir_inactivos:
        statement = select(Progreso)
    else:
        statement = select(Progreso).where(Progreso.activo == True)
    return db.exec(statement).all()

def obtener_progreso(db: Session, nombre: str) -> Optional[Progreso]:
    statement = select(Progreso).where(Progreso.nombre.ilike(nombre))
    return db.exec(statement).first()

def actualizar_progreso(db: Session, nombre: str, nuevo_progreso_data: Progreso) -> Progreso | dict:
    db_progreso = obtener_progreso(db, nombre)
    if db_progreso:
        db_progreso.sqlmodel_update(nuevo_progreso_data.dict(exclude_unset=True))
        db.add(db_progreso)
        db.commit()
        db.refresh(db_progreso)
        return db_progreso
    return {"error": "Progreso no encontrado"}

def eliminar_progreso(db: Session, nombre: str) -> dict:
    db_progreso = obtener_progreso(db, nombre)
    if db_progreso:
        delete_image_file(db_progreso.image_path)
        db_progreso.activo = False
        db.add(db_progreso)
        db.commit()
        db.refresh(db_progreso)
        return {"mensaje": "Progreso marcado como eliminado"}
    return {"error": "Progreso no encontrado"}

def listar_progresos_historial(db: Session) -> List[Progreso]:
    return listar_progresos(db, incluir_inactivos=True)

def guardar_abandono(db: Session, causa_data: CausaAbandono) -> CausaAbandono:
    db.add(causa_data)
    db.commit()
    db.refresh(causa_data)
    return causa_data

def listar_abandonos(db: Session, incluir_inactivos: bool = False) -> List[CausaAbandono]:
    if incluir_inactivos:
        statement = select(CausaAbandono)
    else:
        statement = select(CausaAbandono).where(CausaAbandono.activo == True)
    return db.exec(statement).all()

def obtener_abandono(db: Session, nombre: str) -> Optional[CausaAbandono]:
    statement = select(CausaAbandono).where(CausaAbandono.nombre.ilike(nombre))
    return db.exec(statement).first()

def obtener_abandono_por_motivo(db: Session, motivo: str) -> List[CausaAbandono]:
    statement = select(CausaAbandono).where(CausaAbandono.motivo.ilike(f"%{motivo}%"))
    return db.exec(statement).all()

def actualizar_abandono(db: Session, nombre: str, nueva_causa_data: CausaAbandono) -> CausaAbandono | dict:
    db_causa = obtener_abandono(db, nombre)
    if db_causa:
        db_causa.sqlmodel_update(nueva_causa_data.dict(exclude_unset=True))
        db.add(db_causa)
        db.commit()
        db.refresh(db_causa)
        return db_causa
    return {"error": "Causa de abandono no encontrada"}

def eliminar_abandono(db: Session, nombre: str) -> dict:
    db_causa = obtener_abandono(db, nombre)
    if db_causa:
        db_causa.activo = False
        db.add(db_causa)
        db.commit()
        db.refresh(db_causa)
        return {"mensaje": "Causa de abandono marcada como eliminada"}
    return {"error": "Causa de abandono no encontrada"}

def listar_abandonos_historial(db: Session) -> List[CausaAbandono]:
    return listar_abandonos(db, incluir_inactivos=True)