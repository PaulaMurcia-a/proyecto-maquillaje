from fastapi import FastAPI, HTTPException
from categoria import Categoria
from tipos_piel import TipoPiel
from producto import Producto
from service import *
import csv

app = FastAPI()


@app.get("/")
def home():
    return {"mensaje": "Beauty App funcionando "}



#PRODUCTO


@app.get("/productos")
def listar():
    return get_productos()


@app.get("/productos/{producto_id}")
def obtener(producto_id: int):
    producto = get_producto_by_id(producto_id)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto


@app.post("/productos")
def crear(producto: Producto):
    try:
        create_producto(producto)
        return {"mensaje": "Producto creado"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/productos/{producto_id}")
def actualizar(producto_id: int, producto: Producto):
    actualizado = update_producto(producto_id, producto)

    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto actualizado"}


@app.delete("/productos/{producto_id}")
def eliminar(producto_id: int):
    eliminado = delete_producto(producto_id)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto desactivado"}

#ESTADO

@app.put("/productos/{producto_id}/estado")
def cambiar_estado(producto_id: int, estado: str):

    resultado = cambiar_estado_producto(producto_id, estado)

    if resultado == "no_encontrado":
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if resultado == "invalido":
        raise HTTPException(status_code=400, detail="Estado inválido")

    if resultado == "igual":
        return {"mensaje": f"El producto ya está {estado}"}

    return {"mensaje": f"Estado cambiado a {estado}"}



# FILTROS


@app.get("/productos/piel/{tipo_piel_id}")
def filtrar_piel(tipo_piel_id: int):
    return recomendar_productos(tipo_piel_id)


@app.get("/productos/marca/")
def filtrar( marca: str = None):
    return filtrar_productos( marca)


@app.get("/productos/buscar/")
def buscar(nombre: str):
    return filtrar_productos(nombre=nombre)



# TIPOS DE PIEL


@app.get("/tipos_piel")
def listar_tipos_piel():
    return get_tipos_piel()

@app.get("/tipos_piel/nombre/")
def buscar_tipo(nombre: str):
    return buscar_tipo_piel(nombre)

@app.post("/tipos_piel")
def crear_tipo(tipo: TipoPiel):
    create_tipo_piel(tipo.dict())
    return {"mensaje": "Creado"}


@app.put("/tipos_piel/{tipo_id}")
def actualizar_tipo(tipo_id: int, tipo: TipoPiel):
    if not update_tipo_piel(tipo_id, tipo.dict()):
        raise HTTPException(404, "No encontrado")
    return {"mensaje": "Actualizado"}


@app.delete("/tipos_piel/{tipo_id}")
def eliminar_tipo(tipo_id: int):
    if not delete_tipo_piel(tipo_id):
        raise HTTPException(404, "No encontrado")
    return {"mensaje": "Eliminado"}

#CATEGORIAS

@app.get("/categorias")
def listar_categorias():
    return get_categorias()


@app.post("/categorias")
def crear_categoria(categoria: Categoria):
    try:
        create_categoria(categoria.dict())
        return {"mensaje": "Categoría creada"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/categorias/{cat_id}")
def actualizar_categoria(cat_id: int, categoria: Categoria):
    if not update_categoria(cat_id, categoria.dict()):
        raise HTTPException(404, "No encontrada")
    return {"mensaje": "Actualizada"}

@app.get("/categorias/buscar/")
def buscar_cat(nombre: str):
    return buscar_categoria(nombre)

@app.delete("/categorias/{cat_id}")
def eliminar_categoria(cat_id: int):
    if not delete_categoria(cat_id):
        raise HTTPException(404, "No encontrada")
    return {"mensaje": "Eliminada"}