from fastapi import FastAPI, HTTPException
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
@app.get("/progreso/eliminados", response_model=list[Progreso])
def leer_progresos_eliminados():
    return [p for p in listar_progresos(incluir_inactivos=True) if not p.activo]

@app.get("/progreso/historial", response_model=list[Progreso])
def historial_progreso_total():
    return listar_progresos(incluir_inactivos=True)
@app.post("/progreso/", response_model=Progreso)
def crear_progreso(p: Progreso):
    return guardar_progreso(p)

@app.get("/progreso/", response_model=list[Progreso])
def leer_progresos():
    return listar_progresos()

@app.get("/progreso/{nombre}", response_model=Progreso)
def leer_progreso(nombre: str):
    for prog in listar_progresos_historial():
        if prog.nombre.lower() == nombre.lower():
            return prog
    raise HTTPException(status_code=404, detail="Progreso no encontrado")

@app.put("/progreso/{nombre}", response_model=Progreso)
def actualizar(nombre: str, nuevo: Progreso):
    res = actualizar_progreso(nombre, nuevo)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.delete("/progreso/{nombre}")
def eliminar(nombre: str):
    res = eliminar_progreso(nombre)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.get("/abandono/historial", response_model=list[CausaAbandono])
def historial_abandono_total():
    return listar_abandonos(incluir_inactivos=True)
@app.post("/abandono/", response_model=CausaAbandono)
def crear_abandono(c: CausaAbandono):
    return guardar_abandono(c)

@app.get("/abandono/", response_model=list[CausaAbandono])
def leer_abandonos():
    return listar_abandonos()

@app.get("/abandono/motivo/{motivo}", response_model=list[CausaAbandono])
def buscar_por_motivo(motivo: str):
    return obtener_abandono_por_motivo(motivo)

@app.get("/abandono/{nombre}", response_model=CausaAbandono)
def leer_abandono(nombre: str):
    for causa in listar_abandonos_historial():
        if causa.nombre.lower() == nombre.lower():
            return causa
    raise HTTPException(status_code=404, detail="Causa no encontrada")

@app.put("/abandono/{nombre}", response_model=CausaAbandono)
def actualizar_abandono(nombre: str, nueva: CausaAbandono):
    res = actualizar_abandono(nombre, nueva)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.delete("/abandono/{nombre}")
def eliminar_causa_abandono(nombre: str):
    res = eliminar_abandono(nombre)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.get("/abandono/eliminados", response_model=list[CausaAbandono])
def leer_abandonos_eliminados():
    return [c for c in listar_abandonos(incluir_inactivos=True) if not c.activo]



