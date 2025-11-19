from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def tutor_conversacional(historial):
    """
    historial debe ser una lista de mensajes con:
    { "role": "user"/"assistant", "content": "texto" }
    """


    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Eres un profesor paciente de cálculo diferencial que explica paso a paso."},
            *historial
        ],
        max_tokens=800
    )

    # usar atributo .content en lugar de indexación
    return resp.choices[0].message.content


