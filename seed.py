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
            (TipoPagoEnum.EFECTIVO, Decimal("0.00")),       # sin cargo
            (TipoPagoEnum.TARJETA, Decimal("2.50")),        # 2.5% extra
            (TipoPagoEnum.TRANSFERENCIA, Decimal("0.00")),  # sin cargo
            (TipoPagoEnum.YAPE, Decimal("0.00")),           # sin cargo
            (TipoPagoEnum.PLIN, Decimal("0.00")),           # sin cargo
        ]

        for tipo, cargo in formas:
            # verificamos si ya existe para no duplicar
            existe = session.query(FormaPago).filter_by(tipo=tipo).first()
            if not existe:
                nuevo_forma= (FormaPago(tipo=tipo, cargo_extra=cargo))
                session.add(nuevo_forma)

        session.commit()
        print("Seed de formas de pago completado ✅")

if __name__ == "__main__":
    seed_formas_pago()









if __name__ == "__main__":
    seed_roles()
    seed_formas_pago()

