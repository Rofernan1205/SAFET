# Punto de entrada de aplicación
from database.connection import SessionLocal
from services.role_service import RolServicio



with SessionLocal() as session:
    servicio = RolServicio(session)
    roles = servicio.mostrar_roles()
    for rol in roles:
        print(f"{rol.id} , {rol.nombre}")





