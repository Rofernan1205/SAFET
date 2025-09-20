from repositories.role_repository import RolRepositorio
from sqlalchemy.orm import Session
from models.models import Rol
from schemas.role_schema import RolCrear, RolActualizar, RolSalida
from pydantic import ValidationError

class RolServicio:
    def __init__(self, sesion: Session):
        self.rol_repositorio = RolRepositorio(sesion) # Llamar repositorio y paramétro session DB

    #Listar todos roles
    def mostrar_roles(self) -> list[RolSalida]:
        roles = self.rol_repositorio.listar_roles()
        return [RolSalida.model_validate(rol) for rol in roles]

    # Buscar por ID
    def obtener_id(self, rol_id :int) -> RolSalida | None:
        rol = self.rol_repositorio.buscar_id(rol_id)
        return RolSalida.model_validate(rol) if rol else None

    # Buscar por nombre
    def obtener_nombre(self, rol_nombre :str) -> RolSalida | None:
        rol = self.rol_repositorio.buscar_nombre(rol_nombre)
        return RolSalida.model_validate(rol) if rol else None

    # Crear
    def crear_rol(self, data: RolCrear) -> RolSalida:
        existe = self.rol_repositorio.buscar_id(data.nombre)
        if existe:
            raise ValueError(f"Ya existe un rol con ese nombre {data.nombre}")
        nuevo_rol = Rol(nombre = data.nombre )
        rol_creado = self.rol_repositorio.crear_rol(nuevo_rol)
        return RolSalida.model_validate(rol_creado)

    # Actualizar
    def actualizar_rol(self,rol_id :id , data: RolActualizar) -> RolSalida:
        rol = self.rol_repositorio.buscar_id(rol_id)
        if not rol:
            raise ValueError(f" No se encontro rol {rol_id}")
        rol.nombre = data.nombre
        rol_actualizado = self.rol_repositorio.actualizar_rol(rol)
        return RolSalida.model_validate(rol_actualizado)


    # Eliminar
    def eliminar_rol(self, rol_id :int) -> bool:
        rol = self.rol_repositorio.buscar_id(rol_id)
        if not rol:
            raise ValueError(f"No se encontro rol {rol_id} ")
        return self.rol_repositorio.eliminar_rol(rol)










