# Repositorio de Roles CRUD
# importar modelo Rol
from models.models import Rol
# importar session de la DB
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError




class RolRepositorio:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    # Listar todos los roles
    def listar_roles(self) -> list[Rol] | []: # Significa: “una lista cuyos elementos son instancias de la clase Rol”.
        roles = self.sesion.query(Rol).all()
        return roles if roles  else []

    # Buscar roles por id
    def buscar_id(self, rol_id) -> Rol | None :
        rol =self.sesion.query(Rol).filter_by(id=rol_id).first()
        return rol if rol else None

    # Buscar roles por nombre
    def buscar_nombre(self, rol_nombre) -> Rol | None :
        rol = self.sesion.query(Rol).filter_by(nombre=rol_nombre).first()
        return rol if rol else None

    # Crear rol
    def crear_rol(self, rol: Rol) -> Rol:
        try:
            self.sesion.add(rol)
            self.sesion.commit()
            self.sesion.refresh(rol)  # Obtiene el ID generado por la BD
            return rol
        except IntegrityError:
            self.sesion.rollback()
            raise ValueError("El rol con este nombre ya existe.")



    # Actualizar rol
    def actualizar_rol(self, rol: Rol) -> Rol:

        try:
            self.sesion.commit()
            self.sesion.refresh(rol)
            return rol
        except IntegrityError:
            self.sesion.rollback()
            raise ValueError("No se puede actualizar el rol debido a un conflicto de datos.")

    # Eliminar rol
    def delete(self, rol: Rol) -> bool:
        try:
            self.sesion.delete(rol)
            self.sesion.commit()
            return True
        except Exception:
            self.sesion.rollback()
            return False


















