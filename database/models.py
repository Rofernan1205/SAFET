# Tablas y relaciones de la base de datos

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Text, CheckConstraint, func
from sqlalchemy.orm import relationship # relacion entre modelos a nivel python
from database.connection import Base
from datetime import datetime

# Tablas de la base de datos SAFETDB
# 1. Categorías
class CategoriaProducto(Base):
    __tablename__ = "categorias_productos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100),unique=True, nullable=False, index=True )
    descripcion = Column(String(250))
    productos = relationship("Producto", back_populates="categorias", cascade="all, delete-orphan")



# 2. Sucursales
class Sucursal(Base):
    __tablename__ = "sucursales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20))
    direccion = Column(Text)

    usuario = relationship("Usuario", back_populates="sucursal")
    producto = relationship("Producto", back_populates="sucursal")
    venta = relationship("Venta", back_populates="sucursal")
    compra = relationship("Compra", back_populates="sucursal")


# 3. Proveedores
class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    ruc = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    correo = Column(String(50))
    direccion = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


    compra = relationship("Compra", back_populates="proveedor")


# 4. Clientes
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, unique=True)
    telefono = Column(String(20))
    correo = Column(String(50))
    ruc = Column(String(20))
    dni = Column(String(8))
    direccion = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    venta = relationship("Venta", back_populates="cliente" )

# 5.Formas de Pago
class FormaPago(Base):
    __tablename__ = "formas_pago"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)

    venta = relationship("Venta", back_populates="forma_pago")


# 6. Usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), unique=True, nullable=False)
    usuario = Column(String(15), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    rol = Column(String(25), unique=True, nullable=False)
    telefono = Column(String(20))
    correo = Column(String(50))

    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    sucursal = relationship("Sucursal", back_populates="usuario")
    venta = relationship("Venta", back_populates="usuario")
    compra = relationship("Compra", back_populates="usuario")
    movimiento = relationship("MovimientoInventario", back_populates="usuario")
    ajuste = relationship("AjusteInventario", back_populates="usuario")











