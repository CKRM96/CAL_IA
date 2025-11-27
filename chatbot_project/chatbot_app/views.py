from django.shortcuts import render, redirect
from .chatbot import tutor_conversacional
from .utils import cargar_ejercicios
import random

def detectar_tema(pregunta):
    pregunta = pregunta.lower()

    temas = {
        "Límites": ["límite", "limite", "tender", "tiende a", "l'hopital"],
        "Derivadas": ["derivada", "derivar", "diferenciación", "diferencial"],
        "Regla del producto": ["producto", "multiplicación de funciones"],
        "Regla del cociente": ["cociente", "división de funciones"],
        "Trigonometría": ["seno", "coseno", "tangente", "trigonometría"],
        "Regla de la cadena": ["cadena", "compuesta"],
        "Logaritmos": ["logaritmo", "ln"],
        "Máximos y mínimos": ["máximo", "mínimo", "extremo", "punto crítico"],
        "Pendientes": ["pendiente", "tangente"],
        "Razón de cambio": ["razón de cambio", "tasa de cambio"],
        "Derivación implícita": ["implícita", "implícito"],
        "Optimización": ["optimizar", "optimización"],
        "Exponenciales": ["exponencial", "e^"],
        "Producto": ["producto simple"],
    }

    for tema, palabras in temas.items():
        if any(p in pregunta for p in palabras):
            return tema

    return None


def obtener_ejercicio_por_tema(tema):
    ejercicios = cargar_ejercicios()
    filtrados = [e for e in ejercicios if e["tema"].lower() == tema.lower()]
    return random.choice(filtrados) if filtrados else None


def es_tema_matematicas(pregunta):
    pregunta = pregunta.lower()

    palabras_clave = [
        "límite", "limite", "derivada", "derivar", "integral", "cálculo", "calculo", "función",
        "funciones", "tasa", "razón", "razon", "pendiente", "optimización",
        "máximo", "mínimo", "extremo", "logaritmo", "trigonometría", "cos", "sen",
        "tan", "lim", "dx", "dy", "d/dx", "d/dt", "e^", "polinomio"
    ]

    return any(p in pregunta for p in palabras_clave)


def chat_view(request):

    # Crear historial si no existe
    if "historial" not in request.session:
        request.session["historial"] = []

    historial = request.session["historial"]

    if request.method == "POST":
        pregunta = request.POST.get("pregunta")

        # Guardar mensaje del usuario
        historial.append({"role": "user", "content": pregunta})

        # Validación de tema matemático
        if not es_tema_matematicas(pregunta):
            respuesta_bot = (
                "Lo siento, pero solo puedo ayudarte con temas de **matemáticas** "
                "y **cálculo diferencial**. 😊\n\n"
                "Intenta preguntar algo relacionado con: límites, derivadas, "
                "optimización, tasas de cambio, trigonometría, etc."
            )

            historial.append({"role": "assistant", "content": respuesta_bot})
            request.session["historial"] = historial

            return render(request, "chatbot_app/chat.html", {
                "historial": historial
            })

        # Llamada a Groq
        respuesta_bot = tutor_conversacional(historial)

        # Detección opcional de ejercicio
        tema_detectado = detectar_tema(pregunta)
        if tema_detectado:
            ejercicio = obtener_ejercicio_por_tema(tema_detectado)
            if ejercicio:
                respuesta_bot += f"""

📘 **Ejercicio sugerido sobre {tema_detectado.capitalize()}**
{ejercicio['enunciado']}
"""

        # Guardar respuesta del bot
        historial.append({"role": "assistant", "content": respuesta_bot})
        request.session["historial"] = historial

    return render(request, "chatbot_app/chat.html", {
        "historial": request.session.get("historial", [])
    })


def reset_chat(request):
    request.session["historial"] = [
        {"role": "assistant", "content": "¡Conversación reiniciada! ¿En qué tema de cálculo quieres ayuda ahora?"}
    ]
    return redirect("chat")
