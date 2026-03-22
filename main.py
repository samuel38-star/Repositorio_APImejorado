from fastapi import FastAPI, Body

app = FastAPI()

productos = [
    {"codigo": 1, 
    "nombre": "Arroz", 
    "valor": 2500, 
    "existencias": 20},
    
    {"codigo": 2, 
    "nombre": "Leche", 
    "valor": 3500, 
    "existencias": 15},
    
    {"codigo": 3, 
    "nombre": "Pan", 
    "valor": 1000, 
    "existencias": 30}
]

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido ingeniero"}

@app.get("/productos")
def listProducto():
    return productos

@app.get("/productos/{cod}")
def FindProductos(cod: int):
    if cod <= 0:
        return {"mensaje": "El código debe ser mayor a 0"}

    for prod in productos:
        if prod["codigo"] == cod:
            return prod

    return {"mensaje": "Producto no encontrado"}

@app.post("/productos")
def CrearProductos(data: dict = Body(...)):
    nom = data.get("nombre")
    val = data.get("valor")
    exi = data.get("existencias")
    
    if None in (nom, val, exi):
        return {"mensaje": "Faltan datos"}, print(data)

    if val <= 0 or exi <= 0:
        return {"mensaje": "Valor y existencias deben ser mayores a 0"}

    nuevo_codigo = productos[-1]["codigo"] + 1 if productos else 1

    nuevo_producto = {
        "codigo": nuevo_codigo,
        "nombre": nom,
        "valor": val,
        "existencias": exi
    }

    productos.append(nuevo_producto)

    return {"mensaje": "Producto agregado", "producto": nuevo_producto}

@app.put("/productos/{cod}")
def ActualizarProducto(cod: int, data: dict = Body(...)):
    if cod <= 0:
        return {"mensaje": "El código debe ser mayor a 0"}

    nom = data.get("nombre")
    val = data.get("valor")
    exi = data.get("existencias")

    if None in (nom, val, exi):
        return {"mensaje": "Faltan datos"}

    if val <= 0 or exi <= 0:
        return {"mensaje": "Valor y existencias deben ser mayores a 0"}

    for prod in productos:
        if prod["codigo"] == cod:
            antes = prod.copy()

            prod.update({
                "nombre": nom,
                "valor": val,
                "existencias": exi
            })

            return {"antes": antes, "despues": prod}

    return {"mensaje": "Producto no encontrado"}

@app.delete("/productos/{cod}")
def EliminarProducto(cod: int):
    if cod <= 0:
        return {"mensaje": "El código debe ser mayor a 0"}

    for prod in productos:
        if prod["codigo"] == cod:
            eliminado = prod.copy()
            productos.remove(prod)
            return {"producto_eliminado": eliminado}

    return {"mensaje": "Producto no encontrado"}