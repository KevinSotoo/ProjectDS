from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, Form
from typing import List, Optional
from sqlmodel import Session
from connection_db import get_session
from create_tables import init_db
from models import Progreso, CausaAbandono
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from operations import guardar_progreso, listar_progresos, obtener_progreso, actualizar_progreso, eliminar_progreso, guardar_abandono, listar_abandonos, obtener_abandono, actualizar_abandono, eliminar_abandono, obtener_abandono_por_motivo, listar_progresos_historial, listar_abandonos_historial, save_image_file, delete_image_file


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOADS_DIR = "static/uploads"
Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "titulo": "¡Bienvenido a mi Proyecto FastAPI!"},
    )

@app.on_event("startup")
async def startup_event():
    init_db()



@app.post("/progreso/", response_model=Progreso)
def crear_progreso_sin_imagen(progreso_data: Progreso, db: Session = Depends(get_session)):
    return guardar_progreso(db, progreso_data)


@app.post("/progreso_con_imagen/", response_model=Progreso)
async def crear_progreso_con_imagen(
        nombre: str = Form(...),
        sexo: str = Form(...),
        tiempo_entrenando: str = Form(...),
        objetivo: str = Form(...),
        peso: float = Form(...),
        altura: float = Form(...),
        indice_grasa: float = Form(...),
        edad: int = Form(...),
        image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_session)
):
    image_path = None
    if image:
        image_path = await save_image_file(image)
        if image_path is None:
            raise HTTPException(status_code=500, detail="Error al guardar el archivo de imagen.")

    progreso_data = Progreso(
        nombre=nombre,
        sexo=sexo,
        tiempo_entrenando=tiempo_entrenando,
        objetivo=objetivo,
        peso=peso,
        altura=altura,
        indice_grasa=indice_grasa,
        edad=edad,
        imagen_path=image_path
    )
    return guardar_progreso(db, progreso_data)


@app.put("/progreso/{nombre}/imagen/", response_model=Progreso)
async def actualizar_imagen_progreso(
        nombre: str,
        image: UploadFile = File(...),
        db: Session = Depends(get_session)
):
    progreso_existente = obtener_progreso(db, nombre)
    if not progreso_existente:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")

    delete_image_file(progreso_existente.imagen_path)
    new_image_path = await save_image_file(image)

    if new_image_path is None:
        raise HTTPException(status_code=500, detail="Error al guardar la nueva imagen.")
    progreso_existente.imagen_path = new_image_path

    try:
        db.add(progreso_existente)
        db.commit()
        db.refresh(progreso_existente)
        return progreso_existente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar imagen en DB: {e}")

@app.get("/progreso/", response_model=List[Progreso])
def obtener_progresos(db: Session = Depends(get_session), incluir_inactivos: bool = False):
    return listar_progresos(db, incluir_inactivos)

@app.get("/progreso/{nombre}", response_model=Progreso)
def obtener_progreso_por_nombre(nombre: str, db: Session = Depends(get_session)):
    progreso = obtener_progreso(db, nombre)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@app.put("/progreso/{nombre}", response_model=Progreso)
def actualizar_progreso(nombre: str, progreso_data: Progreso, db: Session = Depends(get_session)):
    updated_progreso = actualizar_progreso(db, nombre, progreso_data)
    if isinstance(updated_progreso, dict) and "error" in updated_progreso:
        raise HTTPException(status_code=404, detail=updated_progreso["error"])
    return updated_progreso

@app.delete("/progreso/{nombre}", response_model=dict)
def delete_progreso(nombre: str, db: Session = Depends(get_session)):
    result = eliminar_progreso(db, nombre)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/progreso_historial/", response_model=List[Progreso])
def  progreso_historial(db: Session = Depends(get_session)):
    return listar_progresos_historial(db)

@app.post("/abandono/", response_model=CausaAbandono)
def crear_abandono(causa_data: CausaAbandono, db: Session = Depends(get_session)):
    return guardar_abandono(db, causa_data)

@app.get("/abandono/", response_model=List[CausaAbandono])
def obtener_abandonos(db: Session = Depends(get_session), incluir_inactivos: bool = False):
    return listar_abandonos(db, incluir_inactivos)

@app.get("/abandono/{nombre}", response_model=CausaAbandono)
def obtener_abandono_por_nombre(nombre: str, db: Session = Depends(get_session)):
    abandono = obtener_abandono(db, nombre)
    if not abandono:
        raise HTTPException(status_code=404, detail="Causa de abandono no encontrada")
    return abandono

@app.get("/abandono_por_motivo/", response_model=List[CausaAbandono])
def abandono_por_motivo(motivo: str, db: Session = Depends(get_session)):
    return obtener_abandono_por_motivo(db, motivo)

@app.put("/abandono/{nombre}", response_model=CausaAbandono)
def actualizar_abandono(nombre: str, causa_data: CausaAbandono, db: Session = Depends(get_session)):
    updated_abandono = actualizar_abandono(db, nombre, causa_data)
    if isinstance(updated_abandono, dict) and "error" in updated_abandono:
        raise HTTPException(status_code=404, detail=updated_abandono["error"])
    return updated_abandono

@app.delete("/abandono/{nombre}", response_model=dict)
def delete_abandono(nombre: str, db: Session = Depends(get_session)):
    result = eliminar_abandono(db, nombre)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/abandono_historial/", response_model=List[CausaAbandono])
def abandono_historial(db: Session = Depends(get_session)):
    return listar_abandonos_historial(db)




