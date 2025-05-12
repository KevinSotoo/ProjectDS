from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from sqlmodel import Session
from connection_db import get_session
from create_tables import init_db
from models import Progreso, CausaAbandono
from operations import (
    guardar_progreso,
    listar_progresos,
    obtener_progreso,
    actualizar_progreso,
    eliminar_progreso,
    guardar_abandono,
    listar_abandonos,
    obtener_abandono,
    actualizar_abandono,
    eliminar_abandono,
    obtener_abandono_por_motivo, listar_progresos_historial, listar_abandonos_historial
)

app = FastAPI()
@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/progreso/", response_model=Progreso)
def crear_progreso_endpoint(progreso_data: Progreso, db: Session = Depends(get_session)):
    return guardar_progreso(db, progreso_data)

@app.get("/progreso/", response_model=List[Progreso])
def get_progresos_endpoint(db: Session = Depends(get_session), incluir_inactivos: bool = False):
    return listar_progresos(db, incluir_inactivos)

@app.get("/progreso/{nombre}", response_model=Progreso)
def get_progreso_por_nombre_endpoint(nombre: str, db: Session = Depends(get_session)):
    progreso = obtener_progreso(db, nombre)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@app.put("/progreso/{nombre}", response_model=Progreso)
def update_progreso_endpoint(nombre: str, progreso_data: Progreso, db: Session = Depends(get_session)):
    updated_progreso = actualizar_progreso(db, nombre, progreso_data)
    if isinstance(updated_progreso, dict) and "error" in updated_progreso:
        raise HTTPException(status_code=404, detail=updated_progreso["error"])
    return updated_progreso

@app.delete("/progreso/{nombre}", response_model=dict)
def delete_progreso_endpoint(nombre: str, db: Session = Depends(get_session)):
    result = eliminar_progreso(db, nombre)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/progreso_historial/", response_model=List[Progreso])
def get_progreso_historial_endpoint(db: Session = Depends(get_session)):
    return listar_progresos_historial(db)

@app.post("/abandono/", response_model=CausaAbandono)
def crear_abandono_endpoint(causa_data: CausaAbandono, db: Session = Depends(get_session)):
    return guardar_abandono(db, causa_data)

@app.get("/abandono/", response_model=List[CausaAbandono])
def get_abandonos_endpoint(db: Session = Depends(get_session), incluir_inactivos: bool = False):
    return listar_abandonos(db, incluir_inactivos)

@app.get("/abandono/{nombre}", response_model=CausaAbandono)
def get_abandono_por_nombre_endpoint(nombre: str, db: Session = Depends(get_session)):
    abandono = obtener_abandono(db, nombre)
    if not abandono:
        raise HTTPException(status_code=404, detail="Causa de abandono no encontrada")
    return abandono

@app.get("/abandono_por_motivo/", response_model=List[CausaAbandono])
def get_abandono_por_motivo_endpoint(motivo: str, db: Session = Depends(get_session)):
    return obtener_abandono_por_motivo(db, motivo)

@app.put("/abandono/{nombre}", response_model=CausaAbandono)
def update_abandono_endpoint(nombre: str, causa_data: CausaAbandono, db: Session = Depends(get_session)):
    updated_abandono = actualizar_abandono(db, nombre, causa_data)
    if isinstance(updated_abandono, dict) and "error" in updated_abandono:
        raise HTTPException(status_code=404, detail=updated_abandono["error"])
    return updated_abandono

@app.delete("/abandono/{nombre}", response_model=dict)
def delete_abandono_endpoint(nombre: str, db: Session = Depends(get_session)):
    result = eliminar_abandono(db, nombre)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/abandono_historial/", response_model=List[CausaAbandono])
def get_abandono_historial_endpoint(db: Session = Depends(get_session)):
    return listar_abandonos_historial(db)



