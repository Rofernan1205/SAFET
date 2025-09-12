# init_db.py
from database.connection import Base, Engine
from models.models import *

def init_db():
    print("Creando tablas...")
    Base.metadata.create_all(bind=Engine)
    print("Tablas creadas exitosamente ✅")

if __name__ == "__main__":
    init_db()
