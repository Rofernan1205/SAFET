# Configuración general (DB, rutas, constantes)
import os

# Configuración de conexión (SQLite para ejemplo real)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///safetdb.db")