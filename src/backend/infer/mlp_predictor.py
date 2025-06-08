import os
import torch
import numpy as np
import joblib
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from scipy.special import softmax
from sklearn.utils.class_weight import compute_class_weight

# Carpeta donde está tu script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sube carpetas hasta llegar al proyecto y entra a "models"
model_path = os.path.join(BASE_DIR, "..", "models", "MLPClassifier_clip_model.pkl")
scaler_path = os.path.join(BASE_DIR, "..", "models", "MLPClassifier_scaler.pkl")
encoder_path = os.path.join(BASE_DIR, "..", "models", "MLPClassifier_label_encoder.pkl")


# Cargar CLIP
#clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
#clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
from transformers import CLIPModel, CLIPProcessor

clip_model = CLIPModel.from_pretrained(
    "/models/hf/clip-vit-base-patch32",
    local_files_only=True
)

clip_processor = CLIPProcessor.from_pretrained(
    "/models/hf/clip-vit-base-patch32",
    local_files_only=True
)



clip_model.eval()

# Cargar modelo entrenado y scaler
mlp = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Cargar LabelEncoder y obtener clases en orden correcto
le = joblib.load(encoder_path)
CLASSES = list(le.classes_)
# Etiquetas que usaste durante el entrenamiento 

def predict_with_mlp(image_path): 
    # Procesar imagen
    image = Image.open(image_path).convert("RGB")
    inputs = clip_processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)

    # Escalar
    vector = scaler.transform(image_features.cpu().numpy())
    
    
    # Predicción
    probs = mlp.predict_proba(vector)[0]
    top_idx = np.argmax(probs)
    top_class = CLASSES[top_idx]

    # Top 3
    top3_idx = probs.argsort()[-3:][::-1]
    top3 = [(CLASSES[i], round(probs[i]*100, 2)) for i in top3_idx]

    #print("Input vector (after scaler):", vector)
    #print("Probs:", probs)

    return top_class, probs[top_idx], {CLASSES[i]: probs[i] for i in top3_idx}
