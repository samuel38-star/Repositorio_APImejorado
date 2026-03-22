from fastapi import FastAPI, Body

app = FastAPI()

productos = [
    {
        "codigo": 1,
        "nombre": "Arroz",
        "valor": 2500,
        "existencias": 20
    },
    {
        "codigo": 2,
        "nombre": "Leche",
        "valor": 3500,
        "existencias": 15
    },
    {
        "codigo": 3,
        "nombre": "Pan",
        "valor": 1000,
        "existencias": 30
    }
]

@app.get("/")
def inicio():
    return {"mensaje": "API de productos funcionando"}

@app.get("/productos")
def listProducto():
    return productos

@app.get("/productos/{cod}")
def FindProductos(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            return prod
    return {"mensaje": "Producto no encontrado"}

@app.get("/productos/nombre/{nom}")
def FindProductos2(nom: str):
    for prod in productos:
        if prod["nombre"].lower() == nom.lower():
            return prod
    return {"mensaje": "Producto no encontrado"}

@app.post("/productos")
def CrearProductos(
    cod: int = Body(...),
    nom: str = Body(...),
    val: float = Body(...),
    exi: int = Body(...)
):
    for prod in productos:
        if prod["codigo"] == cod:
            return {"mensaje": "Ya existe un producto con ese código"}

    nuevo_producto = {
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi
    }

    productos.append(nuevo_producto)
    return {
        "mensaje": "Producto agregado correctamente",
        "productos": productos
    }

@app.put("/productos/{cod}")
def ActualizarProducto(
    cod: int,
    nom: str = Body(...),
    val: float = Body(...),
    exi: int = Body(...)
):
    for prod in productos:
        if prod["codigo"] == cod:
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exi
            return {
                "mensaje": "Producto actualizado correctamente",
                "producto": prod
            }
    return {"mensaje": "Producto no encontrado"}

@app.delete("/productos/{cod}")
def EliminarProducto(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            productos.remove(prod)
            return {
                "mensaje": "Producto eliminado correctamente",
                "productos": productos
            }
    return {"mensaje": "Producto no encontrado"}