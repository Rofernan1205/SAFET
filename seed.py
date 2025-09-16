# Ingresar datos iniciales para la DB
from database.connection import SessionLocal
from models.models import Rol

def seed_roles():
    roles = ["Admin", "Cajero", "Supervisor"]

    # Abrir conexión a la DB
    with SessionLocal() as session:
        for nombre in roles:
            # Verificamos si el rol ya existe para no duplicar
            existe = session.query(Rol).filter_by(nombre=nombre).first()
            if not existe:
                nuevo_rol = Rol(nombre=nombre)
                session.add(nuevo_rol)
                print(f"{nombre} agregado")
            else:
                print(f"Rol {nombre} ya existe, no se inserto")
        session.commit()
        print("Roles agregados")


if __name__ == "__main__":
    seed_roles()

