# src/infer_zero_shot.py

from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
from src.config import CLASSES

device = "cuda" if torch.cuda.is_available() else "cpu"

# Force fallback to slow processor
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to("cuda" if torch.cuda.is_available() else "cpu")

def classify_image(img_path):
    image = Image.open(img_path).convert("RGB")
    inputs = processor(text=CLASSES, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # shape: [1, len(CLASSES)]
    probs = logits_per_image.softmax(dim=1).squeeze()

    pred_index = torch.argmax(probs).item()
    return CLASSES[pred_index], probs.tolist()