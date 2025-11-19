from django.shortcuts import render
from django.shortcuts import redirect
from .chatbot import tutor_conversacional

def chat_view(request):
    # Si no existe historial aún, crearlo
    if "historial" not in request.session:
        request.session["historial"] = []

    respuesta = None

    if request.method == "POST":
        pregunta = request.POST.get("pregunta")

        # Recuperar historial
        historial = request.session["historial"]

        # Agregar la nueva pregunta del usuario
        historial.append({"role": "user", "content": pregunta})

        # Obtener respuesta IA
        respuesta = tutor_conversacional(historial)

        # Guardar la respuesta en el historial
        historial.append({"role": "assistant", "content": respuesta})

        # Actualizar la sesión
        request.session["historial"] = historial

    return render(request, "chatbot_app/chat.html", {
        "historial": request.session.get("historial", [])
    })

def reset_chat(request):
    request.session["historial"] = []
    return redirect("chat")

