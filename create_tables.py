from sqlmodel import SQLModel, create_engine
from models import Progreso, CausaAbandono
from dotenv import load_dotenv
import os


def init_db():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)

    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    init_db()
    print("¡Tablas creadas exitosamente!")