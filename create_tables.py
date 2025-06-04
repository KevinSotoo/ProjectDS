from sqlmodel import SQLModel, create_engine
from models import Progreso, CausaAbandono
from dotenv import load_dotenv
import os

def init_db():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL no encontrada en las variables de entorno")

    engine = create_engine(database_url)

    try:
        print("Creando tablas si no existen...")
        SQLModel.metadata.create_all(engine)
        print("¡Proceso de verificación/creación de tablas completado exitosamente!")

    except Exception as e:
        print(f"Error durante la actualización de la base de datos: {e}")
        raise

if __name__ == "__main__":
    print("Iniciando verificación de la base de datos...")
    init_db()
    print("¡Proceso completado!")
