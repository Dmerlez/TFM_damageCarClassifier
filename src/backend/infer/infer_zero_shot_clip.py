# src/infer/infer_zero_shot.py

from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
from src.config import PROMPTS_BY_CLASS

device = "cuda" if torch.cuda.is_available() else "cpu"

# Modelo y procesador
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

# Generar lista de prompts y su clase asociada
ALL_PROMPTS = []
PROMPT_TO_CLASS = []

for class_name, prompts in PROMPTS_BY_CLASS.items():
    for prompt in prompts:
        ALL_PROMPTS.append(prompt)
        PROMPT_TO_CLASS.append(class_name)

def classify_image(img_path):
    try:
        image = Image.open(img_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Error loading image {img_path}: {e}")

    # Tokenizar imagen y texto
    inputs = processor(text=ALL_PROMPTS, images=image, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=-1).squeeze(0).cpu()

    # Agregar probabilidades por clase
    class_scores = {}
    for prob, class_name in zip(probs, PROMPT_TO_CLASS):
        class_scores[class_name] = class_scores.get(class_name, 0.0) + prob.item()

    # Elegir la clase con mayor score acumulado
    pred_class = max(class_scores, key=class_scores.get)
    return pred_class, class_scores

def main():
    folder_path = "data/val/Intacto/"
    true_class = os.path.basename(os.path.normpath(folder_path))  # Extrae "Intacto"

    for img_name in os.listdir(folder_path):
        if not img_name.lower().endswith(".jpg"):
            continue

        img_path = os.path.join(folder_path, img_name)
        try:
            pred_label, probs = classify_image(img_path)
            print(f"\nImagen: {img_path}")
            print(f"Clase real: {true_class}")
            print(f"Predicción: {pred_label}")
            print(f"Top 3 scores:")
            for class_name, score in sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"  {class_name}: {score:.4f}")
        except Exception as e:
            print(f"Error al procesar {img_path}: {e}")


if __name__ == "__main__":
    main()