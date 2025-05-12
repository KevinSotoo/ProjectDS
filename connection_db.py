import os
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no encontrada en las variables de entorno o en el archivo .env")

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    try:
        print("Intentando conectar a la base de datos y crear/verificar tablas...")
        SQLModel.metadata.create_all(engine)
        print("Tablas de la base de datos creadas/verificadas exitosamente.")
    except Exception as e:
        print(f"ERROR al crear/verificar tablas de la base de datos: {e}")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session