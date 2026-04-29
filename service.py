import pandas as pd
from producto import Producto

FILE = "productos.csv"
TIPOS_FILE = "tipos_piel.csv"
CATEGORIAS_FILE = "categorias.csv"



# GET ALL (solo activos)

def get_productos():
    df = pd.read_csv(FILE)
    return df[df["estado"] == "activo"].to_dict(orient="records")



# PRODUCTO

def create_producto(producto: Producto):
    try:
        df = pd.read_csv(FILE)
    except:
        df = pd.DataFrame(columns=["id","nombre","marca","tipo_piel_id","categoria_id","estado"])

    # ids no duplicados
    if producto.id in df["id"].values:
        raise ValueError("El ID ya existe")

    new_data = {
        "id": producto.id,
        "nombre": producto.nombre,
        "marca": producto.marca,
        "tipo_piel_id": producto.tipo_piel_id,
        "categoria_id": producto.categoria_id,
        "estado": "activo"
    }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(FILE, index=False)


def get_producto_by_id(producto_id: int):
    df = pd.read_csv(FILE)
    result = df[(df["id"] == producto_id) & (df["estado"] == "activo")]
    return result.to_dict(orient="records")


def update_producto(producto_id: int, updated: Producto):
    df = pd.read_csv(FILE)

    if producto_id not in df["id"].values:
        return False

    df.loc[df["id"] == producto_id, ["nombre","marca","tipo_piel_id","categoria_id"]] = [
        updated.nombre,
        updated.marca,
        updated.tipo_piel_id,
        updated.categoria_id
    ]

    df.to_csv(FILE, index=False)
    return True


def cambiar_estado_producto(producto_id: int, estado: str):
    df = pd.read_csv(FILE)

    if producto_id not in df["id"].values:
        return "no_encontrado"

    estado_actual = df.loc[df["id"] == producto_id, "estado"].values[0]


    if estado_actual == estado:
        return "igual"

    if estado not in ["activo", "inactivo"]:
        return "invalido"

    df.loc[df["id"] == producto_id, "estado"] = estado
    df.to_csv(FILE, index=False)

    return "actualizado"


def delete_producto(producto_id: int):
    df = pd.read_csv(FILE)

    if producto_id not in df["id"].values:
        return False

    df.loc[df["id"] == producto_id, "estado"] = "inactivo"

    df.to_csv(FILE, index=False)
    return True



# TIPOS DE PIEL

def recomendar_productos(tipo_piel_id: int):
    df = pd.read_csv(FILE)
    return df[
        (df["tipo_piel_id"] == tipo_piel_id) &
        (df["estado"] == "activo")
    ].to_dict(orient="records")

def buscar_tipo_piel(nombre: str):
    import pandas as pd

    df = pd.read_csv(TIPOS_FILE)

    resultado = df[
        df["nombre"].str.lower().str.contains(nombre.lower())
    ]

    return resultado.to_dict(orient="records")


def create_tipo_piel(tipo):
    df = pd.read_csv(TIPOS_FILE)

    if tipo["id"] in df["id"].values:
        raise ValueError("ID ya existe")

    df = pd.concat([df, pd.DataFrame([tipo])], ignore_index=True)
    df.to_csv(TIPOS_FILE, index=False)


def update_tipo_piel(tipo_id, updated):
    df = pd.read_csv(TIPOS_FILE)

    if tipo_id not in df["id"].values:
        return False

    df.loc[df["id"] == tipo_id, ["nombre","descripcion"]] = [
        updated["nombre"], updated["descripcion"]
    ]

    df.to_csv(TIPOS_FILE, index=False)
    return True


def delete_tipo_piel(tipo_id):
    df = pd.read_csv(TIPOS_FILE)

    if tipo_id not in df["id"].values:
        return False

    df = df[df["id"] != tipo_id]
    df.to_csv(TIPOS_FILE, index=False)
    return True



# FILTRO DINÁMICO

def filtrar_productos(nombre=None, marca=None):
    df = pd.read_csv(FILE)
    df = df[df["estado"] == "activo"]

    if nombre:
        df = df[df["nombre"].str.lower().str.contains(nombre.lower())]

    if marca:
        df = df[df["marca"].str.lower().str.contains(marca.lower())]

    return df.to_dict(orient="records")

#CATEGORIAS

def get_categorias():
    df = pd.read_csv(CATEGORIAS_FILE)
    return df.to_dict(orient="records")


def create_categoria(categoria):
    try:
        df = pd.read_csv(CATEGORIAS_FILE)
    except:
        df = pd.DataFrame(columns=["id", "nombre"])

    if categoria["id"] in df["id"].values:
        raise ValueError("El ID ya existe")

    df = pd.concat([df, pd.DataFrame([categoria])], ignore_index=True)
    df.to_csv(CATEGORIAS_FILE, index=False)


def update_categoria(cat_id, updated):
    df = pd.read_csv(CATEGORIAS_FILE)

    if cat_id not in df["id"].values:
        return False

    df.loc[df["id"] == cat_id, "nombre"] = updated["nombre"]
    df.to_csv(CATEGORIAS_FILE, index=False)
    return True



def buscar_categoria(nombre: str):
    df = pd.read_csv(CATEGORIAS_FILE)
    return df[df["nombre"].str.lower().str.contains(nombre.lower())].to_dict(orient="records")