from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de conexión (SQLite para ejemplo real)
DATABASE_URL = "sqlite:///safetdb.db"

# Motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()






