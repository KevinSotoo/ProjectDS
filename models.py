from typing import Optional
from sqlmodel import Field, SQLModel

class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    sexo: str
    tiempo_entrenando: str
    objetivo: str
    peso: float
    altura: float
    indice_grasa: float
    edad: int
    activo: bool = Field(default=True)
    imagen_path: Optional[str] = Field(default=None)

class CausaAbandono(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    motivo: str
    fecha: str
    detalle: str
    activo: bool = Field(default=True)