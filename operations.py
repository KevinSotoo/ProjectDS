import csv
import os
from models import Progreso, CausaAbandono

DB_PATH_PROGRESO = "database_progresos.csv"
DB_PATH_ABANDONO = "database_abandonos.csv"


def guardar_progreso(progreso: Progreso):
    with open(DB_PATH_PROGRESO, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            progreso.nombre,
            progreso.sexo,
            progreso.tiempo_entrenando,
            progreso.objetivo,
            progreso.peso,
            progreso.altura,
            progreso.indice_grasa,
            progreso.edad,
            progreso.activo  # Nuevo campo
        ])
    return progreso

def listar_progresos(incluir_inactivos=False):
    progresos = []
    if not os.path.exists(DB_PATH_PROGRESO):
        return progresos
    with open(DB_PATH_PROGRESO, mode="r") as file:
        reader = csv.reader(file)
        for fila in reader:
            p = Progreso(
                nombre=fila[0],
                sexo=fila[1],
                tiempo_entrenando=fila[2],
                objetivo=fila[3],
                peso=float(fila[4]),
                altura=float(fila[5]),
                indice_grasa=float(fila[6]),
                edad=int(fila[7]),
                activo=(fila[8].lower() == "true")  # Convertimos a bool
            )
            if incluir_inactivos or p.activo:
                progresos.append(p)
    return progresos

def obtener_progreso(nombre: str):
    for prog in listar_progresos():
        if prog.nombre.lower() == nombre.lower():
            return prog
    return None

def actualizar_progreso(nombre: str, nuevo: Progreso):
    progresos = listar_progresos()
    actualizado = False
    with open(DB_PATH_PROGRESO, mode="w", newline="") as file:
        writer = csv.writer(file)
        for prog in progresos:
            if prog.nombre.lower() == nombre.lower():
                prog = nuevo
                actualizado = True
            writer.writerow(prog.dict().values())
    if actualizado:
        return nuevo
    return {"error": "Progreso no encontrado"}

def eliminar_progreso(nombre: str):
    progresos = listar_progresos(incluir_inactivos=True)
    actualizado = False
    with open(DB_PATH_PROGRESO, mode="w", newline="") as file:
        writer = csv.writer(file)
        for prog in progresos:
            if prog.nombre.lower() == nombre.lower():
                prog.activo = False
                actualizado = True
            writer.writerow(prog.dict().values())
    if actualizado:
        return {"mensaje": "Progreso marcado como eliminado"}
    return {"error": "Progreso no encontrado"}


def guardar_abandono(causa: CausaAbandono):
    with open(DB_PATH_ABANDONO, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            causa.nombre,
            causa.motivo,
            causa.fecha,
            causa.detalle,
            causa.activo  # Nuevo campo
        ])
    return causa

def listar_abandonos(incluir_inactivos=False):
    abandonos = []
    if not os.path.exists(DB_PATH_ABANDONO):
        return abandonos
    with open(DB_PATH_ABANDONO, mode="r") as file:
        reader = csv.reader(file)
        for fila in reader:
            a = CausaAbandono(
                nombre=fila[0],
                motivo=fila[1],
                fecha=fila[2],
                detalle=fila[3],
                activo=(fila[4].lower() == "true")
            )
            if incluir_inactivos or a.activo:
                abandonos.append(a)
    return abandonos

def obtener_abandono(nombre: str):
    for causa in listar_abandonos():
        if causa.nombre.lower() == nombre.lower():
            return causa
    return None

def obtener_abandono_por_motivo(motivo: str):
    return [c for c in listar_abandonos() if motivo.lower() in c.motivo.lower()]

def actualizar_abandono(nombre: str, nueva: CausaAbandono):
    abandonos = listar_abandonos()
    actualizado = False
    with open(DB_PATH_ABANDONO, mode="w", newline="") as file:
        writer = csv.writer(file)
        for causa in abandonos:
            if causa.nombre.lower() == nombre.lower():
                causa = nueva
                actualizado = True
            writer.writerow(causa.dict().values())
    if actualizado:
        return nueva
    return {"error": "Causa de abandono no encontrada"}

def eliminar_abandono(nombre: str):
    abandonos = listar_abandonos(incluir_inactivos=True)
    actualizado = False
    with open(DB_PATH_ABANDONO, mode="w", newline="") as file:
        writer = csv.writer(file)
        for causa in abandonos:
            if causa.nombre.lower() == nombre.lower():
                causa.activo = False
                actualizado = True
            writer.writerow(causa.dict().values())
    if actualizado:
        return {"mensaje": "Causa de abandono marcada como eliminada"}
    return {"error": "Causa de abandono no encontrada"}

def listar_progresos_historial():
    return listar_progresos(incluir_inactivos=True)

def listar_abandonos_historial():
    return listar_abandonos(incluir_inactivos=True)