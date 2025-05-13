import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

from src.config import CLASSES

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def encode_image(image_path: str) -> str:
    """Converts an image to base64 format for OpenAI Vision API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def classify_image_chatgpt(image_path: str) -> str:
    """Classifies vehicle damage using GPT-4 Vision via OpenAI Python SDK v1+."""
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a vehicle damage classification assistant."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Classify the visible damage on the car hood. "
                                f"Choose one of: {', '.join(CLASSES)}. "
                                f"Respond only with the class name."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=10
    )

    return response.choices[0].message.content.strip()