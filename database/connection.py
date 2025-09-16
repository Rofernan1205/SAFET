from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL
import os
from dotenv import load_dotenv

load_dotenv()



# Motor de conexión
Engine = create_engine(DATABASE_URL, echo=True, future=True)

# Sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# Clase base para los modelos ORM
Base = declarative_base()
