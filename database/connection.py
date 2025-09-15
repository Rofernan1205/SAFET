from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de conexión (SQLite para ejemplo real)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///safetdb.db")

# Motor de conexión
Engine = create_engine(DATABASE_URL, echo=True, future=True)

# Sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# Clase base para los modelos
Base = declarative_base()
