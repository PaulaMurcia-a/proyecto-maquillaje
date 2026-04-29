from pydantic import BaseModel

class TipoPiel(BaseModel):
    id: int
    nombre: str
    descripcion: str