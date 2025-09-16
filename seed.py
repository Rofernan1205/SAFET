# Ingresar datos iniciales para la DB
from decimal import Decimal
from database.connection import SessionLocal
from models.models import Rol

def seed_roles():
    roles = ["Admin", "Cajero", "Supervisor"]

    # Abrir la sesión
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


# Formas de pago
from models.models import FormaPago, TipoPagoEnum

def seed_formas_pago():
    # abrimos la sesión
    with SessionLocal() as session:
        # lista de formas de pago iniciales
        formas = [
            (TipoPagoEnum.EFECTIVO.value, Decimal("0.00")),       # sin cargo
            (TipoPagoEnum.TARJETA.value, Decimal("5")),        # 2.5% extra
            (TipoPagoEnum.TRANSFERENCIA.value, Decimal("0.00")),  # sin cargo
            (TipoPagoEnum.YAPE.value, Decimal("0.00")),           # sin cargo
            (TipoPagoEnum.PLIN.value, Decimal("0.00")),           # sin cargo
        ]

        for tipo, cargo in formas:
            # verificamos si ya existe para no duplicar
            existe = session.query(FormaPago).filter_by(tipo=tipo).first()
            if not existe:
                nuevo_forma= (FormaPago(tipo=tipo, cargo_extra=cargo))
                session.add(nuevo_forma)
                print(f"{tipo} agregado")
            else:
                print(f"El metodo {tipo} ya existe")

        session.commit()
        print("Seed de formas de pago completado")


# Sucursales
from models.models import Sucursal


def seed_sucursal():
    with SessionLocal() as session:
        sucursales = [
            ("CP huarapari", "971671606", "Plaza principal")
        ]

        for nombre, telefono, direccion in sucursales:
            existe = session.query(Sucursal).filter_by(nombre=nombre).first()
            if not existe:
                nueva = Sucursal(
                    nombre=nombre,
                    telefono=telefono,
                    direccion=direccion
                )
                session.add(nueva)
                print(f"{nombre} agregado")
            else:
                print(f"La sede {nombre} ya existe")

        session.commit()
        print("Seed de sucursales completado ")

# Categorias

# seed_categorias.py
from models.models import CategoriaProducto
def seed_categoria():
    with SessionLocal() as session:
        categorias = [
            ("Alimentos", "Productos de consumo alimenticio"),
            ("Bebidas", "Gaseosas, jugos y bebidas alcohólicas"),
            ("Limpieza", "Artículos de limpieza y aseo"),
            ("Higiene", "Productos de higiene personal"),
        ]

        for nombre, descripcion in categorias:
            existe = session.query(CategoriaProducto).filter_by(nombre=nombre).first()
            if not existe:
                nueva = CategoriaProducto(nombre=nombre, descripcion=descripcion)
                session.add(nueva)
            else:
                print(f"La categoria {nombre} ya existe")

        session.commit()
        print("Seed de categorías completado")



if __name__ == "__main__":
    # seed_roles()
    # seed_formas_pago()
    # seed_sucursal()
    seed_categoria()

