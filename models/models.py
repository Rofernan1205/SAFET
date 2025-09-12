# ========================================================
# MODELOS SAFETDB - versión profesional
# ========================================================

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric, Text,
    CheckConstraint, func, Boolean, Date, Enum, Index
)
from sqlalchemy.orm import relationship, declarative_mixin
import enum
from database.connection import Base


# ========================================================
# ENUMS para valores controlados
# ========================================================
class EstadoVentaEnum(enum.Enum):
    PENDIENTE = "Pendiente"
    COMPLETADA = "Completada"
    ANULADA = "Anulada"


class TipoFacturaEnum(enum.Enum):
    BOLETA = "Boleta"
    FACTURA = "Factura"
    TICKET = "Ticket"


class TipoMovimientoEnum(enum.Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"


class TipoPagoEnum(enum.Enum):
    EFECTIVO = "Efectivo"
    TARJETA = "Tarjeta"
    TRANSFERENCIA = "Transferencia"
    YAPE = "Yape"
    PLIN = "Plin"


# ========================================================
# MIXIN para timestamps
# ========================================================
@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


# ========================================================
# MIXIN para soft delete
# ========================================================
@declarative_mixin
class SoftDeleteMixin:
    is_active = Column(Boolean, default=True, nullable=False)


# ========================================================
# 1. Categorías
# ========================================================
class CategoriaProducto(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "categorias_productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(String(250))

    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")


# ========================================================
# 2. Roles
# ========================================================
class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)

    usuarios = relationship("Usuario", back_populates="rol")


# ========================================================
# 3. Sucursales
# ========================================================
class Sucursal(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), unique=True)
    direccion = Column(Text)

    usuarios = relationship("Usuario", back_populates="sucursal")
    productos = relationship("Producto", back_populates="sucursal")
    ventas = relationship("Venta", back_populates="sucursal")
    compras = relationship("Compra", back_populates="sucursal")


# ========================================================
# 4. Proveedores
# ========================================================
class Proveedor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    ruc = Column(String(20), unique=True)
    telefono = Column(String(20), unique=True)
    correo = Column(String(50), unique=True)
    direccion = Column(Text)

    compras = relationship("Compra", back_populates="proveedor")


# ========================================================
# 5. Clientes
# ========================================================
class Cliente(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, index=True)
    telefono = Column(String(20), unique=True)
    correo = Column(String(50), unique=True)
    ruc = Column(String(20), unique=True)
    dni = Column(String(8), unique=True)
    direccion = Column(Text)

    ventas = relationship("Venta", back_populates="cliente")


# ========================================================
# 6. Formas de Pago
# ========================================================
class FormaPago(Base, SoftDeleteMixin):
    __tablename__ = "formas_pago"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(Enum(TipoPagoEnum), unique=True, nullable=False, index=True)
    cargo_extra = Column(Numeric(5, 2), default=0, nullable=False)
    # ejemplo: 0 = sin cargo, 2.50 = 2.5% adicional por tarjeta

    ventas = relationship("Venta", back_populates="forma_pago")

    __table_args__ = (
        CheckConstraint("cargo_extra >= 0", name="check_cargo_extra_no_negativo"),
    )


# ========================================================
# 7. Usuarios
# ========================================================
class Usuario(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    usuario = Column(String(15), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    telefono = Column(String(20), unique=True)
    correo = Column(String(50), unique=True)

    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))
    rol_id = Column(Integer, ForeignKey("roles.id"))

    sucursal = relationship("Sucursal", back_populates="usuarios")
    rol = relationship("Rol", back_populates="usuarios")
    ventas = relationship("Venta", back_populates="usuario")
    compras = relationship("Compra", back_populates="usuario")
    movimientos = relationship("MovimientoInventario", back_populates="usuario")
    ajustes = relationship("AjusteInventario", back_populates="usuario")


# ========================================================
# 8. Productos
# ========================================================
class Producto(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), unique=True, nullable=False, index=True)
    marca = Column(String(150))
    codigo_barras = Column(String(50), unique=True)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    costo = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    fecha_vencimiento = Column(Date)
    imagen = Column(String)

    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))
    categoria_id = Column(Integer, ForeignKey("categorias_productos.id", ondelete="CASCADE"))

    __table_args__ = (
        CheckConstraint("precio >= 0", name="check_precio_no_negativo"),
        CheckConstraint("costo >= 0", name="check_costo_no_negativo"),
        CheckConstraint("stock >= 0", name="check_stock_no_negativo"),
    )

    categoria = relationship("CategoriaProducto", back_populates="productos")
    sucursal = relationship("Sucursal", back_populates="productos")
    detalle_ventas = relationship("DetalleVenta", back_populates="producto")
    detalle_compras = relationship("DetalleCompra", back_populates="producto")
    movimientos = relationship("MovimientoInventario", back_populates="producto")
    ajustes = relationship("AjusteInventario", back_populates="producto")


# ========================================================
# 9. Ventas
# ========================================================
class Venta(Base, TimestampMixin):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=func.now(), index=True)
    estado = Column(Enum(EstadoVentaEnum), default=EstadoVentaEnum.COMPLETADA, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    forma_pago_id = Column(Integer, ForeignKey("formas_pago.id"))
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))

    forma_pago = relationship("FormaPago", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    sucursal = relationship("Sucursal", back_populates="ventas")
    usuario = relationship("Usuario", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="venta", uselist=False)


# ========================================================
# 10. Detalle Venta
# ========================================================
class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)

    venta_id = Column(Integer, ForeignKey("ventas.id", ondelete="CASCADE"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad_venta_positiva"),
    )

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_ventas")


# ========================================================
# 11. Compras
# ========================================================
class Compra(Base, TimestampMixin):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=func.now(), index=True)
    total = Column(Numeric(12, 2), nullable=False)

    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))

    proveedor = relationship("Proveedor", back_populates="compras")
    usuario = relationship("Usuario", back_populates="compras")
    sucursal = relationship("Sucursal", back_populates="compras")
    detalles = relationship("DetalleCompra", back_populates="compra", cascade="all, delete-orphan")


# ========================================================
# 12. Detalle Compra
# ========================================================
class DetalleCompra(Base):
    __tablename__ = "detalle_compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)

    compra_id = Column(Integer, ForeignKey("compras.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad_compra_positiva"),
    )

    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_compras")


# ========================================================
# 13. Movimiento Inventario
# ========================================================
class MovimientoInventario(Base, TimestampMixin):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(Enum(TipoMovimientoEnum), nullable=False)
    cantidad = Column(Integer, nullable=False)
    referencia = Column(String(200))
    fecha = Column(DateTime, default=func.now(), index=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad_movimiento_positiva"),
    )

    usuario = relationship("Usuario", back_populates="movimientos")
    producto = relationship("Producto", back_populates="movimientos")


# ========================================================
# 14. Ajuste Inventario
# ========================================================
class AjusteInventario(Base, TimestampMixin):
    __tablename__ = "ajustes_inventario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    motivo = Column(String(200), nullable=False)
    cantidad_ajustada = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=func.now())

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    __table_args__ = (
        CheckConstraint("cantidad_ajustada != 0", name="check_cantidad_ajustada_no_cero"),
    )

    usuario = relationship("Usuario", back_populates="ajustes")
    producto = relationship("Producto", back_populates="ajustes")


# ========================================================
# 15. Factura
# ========================================================

class Factura(Base, TimestampMixin):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_factura = Column(String(50), unique=True, nullable=False, index=True)
    tipo = Column(Enum(TipoFacturaEnum), nullable=False, default=TipoFacturaEnum.BOLETA)
    fecha = Column(DateTime, default=func.now(), index=True)

    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)

    venta = relationship("Venta", back_populates="factura", uselist=False)