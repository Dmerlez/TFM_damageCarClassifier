import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

from config import CLASSES

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



def encode_image(image_path: str) -> str:
    """Converts an image to base64 format for OpenAI Vision API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def predict_with_chatgpt(image_path: str) -> str:
    """Classifies vehicle damage using GPT-4 Vision via OpenAI Python SDK v1+."""
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(model="gpt-4o", messages=[
        {
        "role": "system",
        "content": "Eres un sistema experto en inspección visual de vehículos. "
                   "A continuación, se te mostrará una imagen del lateral, frontal o parte trasera de un vehículo. "
                   "Tu tarea consiste en analizar visualmente el estado de la carrocería y clasificar "
                   "el tipo de daño predominante en una única de las predefinidas categorías."
    },
        {
        "role": "user",
            "content": [{
                         "type": "text",
                         "text": f"Tu tarea consiste en analizar visualmente el estado de la carrocería y clasificar "
                   "el tipo de daño predominante en una única de las predefinidas categorías: {', '.join(CLASSES)}. "             
                   "Abolladura: deformación clara de la chapa sin roturas graves, generalmente localizada en un panel (puerta, guardabarros, capó, etc.)."
                   "Rayón: arañazos visibles, marcas lineales o pérdida de pintura superficial sin alteración en la forma del panel."
                   "Siniestro: daños estructurales o múltiples zonas afectadas con señales de colisión severa, partes desprendidas, desalineaciones, cristales rotos o deformaciones graves."
                   "Intacto: el vehículo no muestra ningún daño visible, abolladura, rallón ni rotura aparente."
                   "No generes explicaciones, solo responde con una de estas cuatro palabras"
                   "Abolladuras, Rayones, Siniestro o Intacto."
                   "También debes responder con la probabilidad la cual estás obteniendo la etiqueta elegida, esta se debe mostrar al lado de la etiqueta, el formato del porcentaje debe ser así, ejemplo: 90%"
                   "El formato con que debe ir la etiqueta y el porcentaje es: Abolladuras 90%"
                   "Evalúa toda el área visible del vehículo, pero si hay duda entre dos categorías, elige la de mayor gravedad."},
                {"type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                 }
            ]
        }
    ],max_tokens=10)

    raw_response = response.choices[0].message.content.strip()

    try:
        label, confidence = raw_response.rsplit(" ", 1)
    except ValueError:
        label, confidence = raw_response, None

    return label, confidence