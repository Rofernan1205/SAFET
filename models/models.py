# ========================================================
# MODELOS SAFETDB - versión final
# ========================================================

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric, Text,
    CheckConstraint, func, Boolean, Date, Enum, Index, PrimaryKeyConstraint
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
    CREDITO = "Crédito"
    APARTADA = "Apartada"


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
    cajas = relationship("Caja", back_populates="sucursal")


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

    # ----- RELACIONES CORREGIDAS -----
    cajas_abiertas = relationship("Caja", foreign_keys="Caja.usuario_apertura_id", back_populates="usuario_apertura")
    cajas_cerradas = relationship("Caja", foreign_keys="Caja.usuario_cierre_id", back_populates="usuario_cierre")



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
    impuestos = relationship("ImpuestoProducto", back_populates="producto")


# ========================================================
# 9. Ventas
# ========================================================
class Venta(Base, TimestampMixin):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=func.now(), index=True)
    estado = Column(Enum(EstadoVentaEnum), default=EstadoVentaEnum.COMPLETADA, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    total_pagado = Column(Numeric(10, 2), default=0, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    forma_pago_id = Column(Integer, ForeignKey("formas_pago.id"))
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))
    caja_id = Column(Integer, ForeignKey("cajas.id"))

    forma_pago = relationship("FormaPago", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    sucursal = relationship("Sucursal", back_populates="ventas")
    usuario = relationship("Usuario", back_populates="ventas")
    caja = relationship("Caja", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="venta", uselist=False)
    pagos = relationship("Pago", back_populates="venta", cascade="all, delete-orphan")


# ========================================================
# 10. Detalle Venta
# ========================================================
class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    margen_ganancia = Column(Numeric(12, 2))

    venta_id = Column(Integer, ForeignKey("ventas.id", ondelete="CASCADE"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad_venta_positiva"),
    )

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_ventas")
    impuestos_detalle = relationship("DetalleImpuestoVenta", back_populates="detalle_venta", cascade="all, delete-orphan")


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
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    compra_id = Column(Integer, ForeignKey("compras.id"))

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad_movimiento_positiva"),
    )

    usuario = relationship("Usuario", back_populates="movimientos")
    producto = relationship("Producto", back_populates="movimientos")
    venta = relationship("Venta")
    compra = relationship("Compra")


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
    tipo_comprobante_id = Column(Integer, ForeignKey("tipos_comprobantes.id"))

    venta = relationship("Venta", back_populates="factura", uselist=False)
    tipo_comprobante = relationship("TipoComprobante", back_populates="facturas")




# ========================================================
# 16. Cajas
# ========================================================
class Caja(Base, TimestampMixin):
    __tablename__ = "cajas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_apertura = Column(DateTime, default=func.now(), nullable=False)
    fecha_cierre = Column(DateTime)
    fondo_inicial = Column(Numeric(10, 2), nullable=False)
    ventas_en_efectivo = Column(Numeric(10, 2), default=0, nullable=False)
    entradas_adicionales = Column(Numeric(10, 2), default=0, nullable=False)
    salidas_adicionales = Column(Numeric(10, 2), default=0, nullable=False)
    balance_final = Column(Numeric(10, 2))
    estado = Column(String(50), default="Abierta", nullable=False)

    usuario_apertura_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario_cierre_id = Column(Integer, ForeignKey("usuarios.id"))
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))

    # ----- RELACIONES CORREGIDAS -----
    usuario_apertura = relationship("Usuario", foreign_keys="Caja.usuario_apertura_id", back_populates="cajas_abiertas")
    usuario_cierre = relationship("Usuario", foreign_keys="Caja.usuario_cierre_id", back_populates="cajas_cerradas")
    sucursal = relationship("Sucursal", back_populates="cajas")
    ventas = relationship("Venta", back_populates="caja")
    pagos = relationship("Pago", back_populates="caja")



# ========================================================
# 17. Parámetros de la Empresa
# ========================================================
class ParametrosEmpresa(Base):
    __tablename__ = "parametros_empresa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_comercial = Column(String(200), nullable=False)
    razon_social = Column(String(200))
    ruc = Column(String(20), unique=True, nullable=False)
    direccion_fiscal = Column(Text)
    telefono = Column(String(20))
    moneda_simbolo = Column(String(5), default="S/.")
    impuesto_general_ventas = Column(Numeric(5, 2), default=18.0)


# ========================================================
# 18. Tipos de Comprobantes
# ========================================================
class TipoComprobante(Base, SoftDeleteMixin):
    __tablename__ = "tipos_comprobantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    serie = Column(String(10), nullable=False)
    correlativo_actual = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        Index("idx_serie_correlativo", "serie", "correlativo_actual"),
    )

    facturas = relationship("Factura", back_populates="tipo_comprobante")

# ========================================================
# 19. Impuestos
# ========================================================
class Impuesto(Base):
    __tablename__ = "impuestos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    porcentaje = Column(Numeric(5, 2), nullable=False)

    productos_relacion = relationship("ImpuestoProducto", back_populates="impuesto", cascade="all, delete-orphan")
    detalles_venta = relationship("DetalleImpuestoVenta", back_populates="impuesto", cascade="all, delete-orphan")

# ========================================================
# 20. Relación Producto-Impuesto
# ========================================================
class ImpuestoProducto(Base):
    __tablename__ = "impuestos_productos"
    __table_args__ = (
        PrimaryKeyConstraint('producto_id', 'impuesto_id'),
    )

    producto_id = Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"))
    impuesto_id = Column(Integer, ForeignKey("impuestos.id", ondelete="CASCADE"))

    producto = relationship("Producto", back_populates="impuestos")
    impuesto = relationship("Impuesto", back_populates="productos_relacion")

# ========================================================
# 21. Detalle de Impuestos en Venta
# ========================================================
class DetalleImpuestoVenta(Base):
    __tablename__ = "detalle_impuestos_venta"
    __table_args__ = (
        PrimaryKeyConstraint('detalle_venta_id', 'impuesto_id'),
    )

    detalle_venta_id = Column(Integer, ForeignKey("detalle_ventas.id", ondelete="CASCADE"))
    impuesto_id = Column(Integer, ForeignKey("impuestos.id", ondelete="CASCADE"))
    monto_impuesto = Column(Numeric(10, 2), nullable=False)

    detalle_venta = relationship("DetalleVenta", back_populates="impuestos_detalle")
    impuesto = relationship("Impuesto", back_populates="detalles_venta")


# ========================================================
# 22. Pagos
# ========================================================
class Pago(Base, TimestampMixin):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    monto_pagado = Column(Numeric(10, 2), nullable=False)
    fecha_pago = Column(DateTime, default=func.now(), nullable=False)
    tipo_pago = Column(Enum(TipoPagoEnum), nullable=False)

    venta_id = Column(Integer, ForeignKey("ventas.id"))
    caja_id = Column(Integer, ForeignKey("cajas.id"))

    venta = relationship("Venta", back_populates="pagos")
    caja = relationship("Caja", back_populates="pagos")