import os
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel
from pathlib import Path

# Config
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Ruta a dataset (subcarpetas por clase)
BASE_DIR = Path(__file__).resolve().parent

# Subir tres niveles y entrar en 'data/all'
DATASET_DIR = BASE_DIR.parents[2] / "data" / "all"
X = []
y = []

for class_name in sorted(os.listdir(DATASET_DIR)):
    class_path = os.path.join(DATASET_DIR, class_name)
    
    if not os.path.isdir(class_path):
        continue

    for img_file in tqdm(os.listdir(class_path), desc=f"Procesando {class_name}"):
        if not img_file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(class_path, img_file)
        try:
            image = Image.open(img_path).convert("RGB")
            inputs = clip_processor(images=image, return_tensors="pt").to(device)
            with torch.no_grad():
                features = clip_model.get_image_features(**inputs)
                features = features / features.norm(p=2, dim=-1, keepdim=True)
            X.append(features.cpu().numpy().flatten())
            y.append(class_name)
        except Exception as e:
            print(f"Error en {img_path}: {e}")

# Guardar
# Ruta base del script actual
BASE_DIR = Path(__file__).resolve().parent

# Ruta a la carpeta models (sube tres niveles desde src/backend/infer)
models_dir = BASE_DIR.parents[2] / "models"

# Guardar los archivos
np.save(models_dir / "X_clip.npy", np.array(X))
np.save(models_dir / "y_labels.npy", np.array(y))

print("✅ Embeddings guardados como 'X_clip.npy' y 'y_labels.npy'")
