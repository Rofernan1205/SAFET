# Repositorio de Roles CRUD

from models.models import Rol
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class RolRepositorio:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    # Listar todos los roles
    def listar_roles(self) -> list[Rol]:
        return self.sesion.query(Rol).all()

    # Buscar rol por ID
    def buscar_id(self, rol_id: int) -> Rol | None:
        return self.sesion.query(Rol).filter_by(id=rol_id).first()

    # Buscar rol por nombre
    def buscar_nombre(self, rol_nombre: str) -> Rol | None:
        return self.sesion.query(Rol).filter_by(nombre=rol_nombre).first()

    # Crear rol
    def crear_rol(self, rol: Rol) -> Rol:
        try:
            self.sesion.add(rol)
            self.sesion.commit()
            self.sesion.refresh(rol)  # Para obtener ID autogenerado
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
    def eliminar_rol(self, rol: Rol) -> bool:
        try:
            self.sesion.delete(rol)
            self.sesion.commit()
            return True
        except Exception:
            self.sesion.rollback()
            return False
