from pydantic import BaseModel

class Progreso(BaseModel):
    nombre: str
    sexo: str
    tiempo_entrenando: str
    objetivo: str
    peso: float
    altura: float
    indice_grasa: float
    edad: int
    activo: bool = True

class CausaAbandono(BaseModel):
    nombre: str
    motivo: str
    fecha: str
    detalle: str
    activo: bool = True
