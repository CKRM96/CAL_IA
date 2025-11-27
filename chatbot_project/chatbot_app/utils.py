import json
import os

def cargar_ejercicios():
    ruta = os.path.join(os.path.dirname(__file__), "ejercicios.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)
