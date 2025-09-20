from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class RolCrear(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)


class RolActualizar(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)


class RolSalida(BaseModel):
    id:int
    nombre:str

    class Config:
        from_attributes = True # se encarga de serializar



