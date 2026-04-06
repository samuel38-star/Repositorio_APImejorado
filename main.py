from fastapi import FastAPI, Body
import json

app = FastAPI()
ARCHIVO = "productos.json"

def cargar_productos():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_productos(productos):
    with open(ARCHIVO, "w") as f:
        json.dump(productos, f, indent=4)

productos = cargar_productos()

@app.get("/")
def inicio():
    return {"mensaje": "API de productos funcionando"}

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
def CrearProductos(data: dict = Body(default={})):  

    print("DATA:", data)  

    nom = data.get("nombre")
    val = data.get("valor")
    exi = data.get("existencias")

    print(nom, val, exi)  

    if nom is None or val is None or exi is None:
        return {
            "mensaje": "Faltan datos",
            "recibido": data   
        }

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
    guardar_productos(productos)
    return {
        "mensaje": "Producto agregado correctamente",
        "producto": nuevo_producto
    }

@app.put("/productos/{cod}")
def ActualizarProducto(cod: int, data: dict = Body(default={})):

    print("DATA:", data)

    if cod <= 0:
        return {"mensaje": "El código debe ser mayor a 0"}

    nom = data.get("nombre")
    val = data.get("valor")
    exi = data.get("existencias")

    if nom is None or val is None or exi is None:
        return {
            "mensaje": "Faltan datos",
            "recibido": data
        }

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
            guardar_productos(productos) 
            return {
                "mensaje": "Producto actualizado",
                "antes": antes,
                "despues": prod
            }
            
    return {"mensaje": "Producto no encontrado"}

@app.delete("/productos/{cod}")
def EliminarProducto(cod: int):
    if cod <= 0:
        return {"mensaje": "El código debe ser mayor a 0"}

    for prod in productos:
        if prod["codigo"] == cod:
            eliminado = prod.copy()
            productos.remove(prod)
            guardar_productos(productos)  
            return {
                "mensaje": "Producto eliminado",
                "producto": eliminado
            }

    return {"mensaje": "Producto no encontrado"}