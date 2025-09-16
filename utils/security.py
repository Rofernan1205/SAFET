from passlib.context import CryptContext
# bcrypt==4.0.1 version funcional

# 1. Creamos un contexto de encriptación, indicando que usaremos "bcrypt"
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Función para hashear (encriptar) una contraseña
def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

# 3. Función para verificar si una contraseña ingresada coincide con el hash guardado
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


# Prueba de funcionamiento

my_password = "prueba123"

password_hash = hash_password(my_password)

salida = verify_password("prueba123", password_hash)
print(salida)