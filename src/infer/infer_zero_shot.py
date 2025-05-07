# src/infer/infer_zero_shot.py
import os
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from src.config import CLASSES_ZERO_SHOT

device = "cuda" if torch.cuda.is_available() else "cpu"
 
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

def classify_image(img_path, threshold=0.1):
    try:
        image = Image.open(img_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Error al cargar la imagen {img_path}: {e}")

    inputs = processor(text=CLASSES_ZERO_SHOT, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).squeeze()

    pred_index = torch.argmax(probs).item()
    max_prob = probs[pred_index].item()

    if max_prob < threshold:
        return "indeterminado", probs.tolist()

    return CLASSES_ZERO_SHOT[pred_index], probs.tolist()

def main():
    val_dir = "data/val"

    for class_folder in os.listdir(val_dir):
        class_path = os.path.join(val_dir, class_folder)
        if not os.path.isdir(class_path):
            continue

        for img_name in os.listdir(class_path):
            if not img_name.lower().endswith(".jpg"):
                continue

            img_path = os.path.join(class_path, img_name)
            try:
                pred_label, probs = classify_image(img_path)
                print(f"\nImagen: {img_path}")
                print(f"Clase real: {class_folder}")
                print(f"Predicción: {pred_label}")
                print(f"Probabilidades: {probs}")
            except Exception as e:
                print(f"Error al procesar {img_path}: {e}")

if __name__ == "__main__":
    main()
