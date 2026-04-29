from pydantic import BaseModel

class Producto(BaseModel):
    id: int
    nombre: str
    marca: str
    tipo_piel_id: int
    categoria_id: int
