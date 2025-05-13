import os
from PIL import Image
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from transformers import CLIPProcessor, CLIPModel
import torch

# ---- CONFIG ----
CLASSES = ["Abolladuras", "Intacto", "Rallones", "Siniestro"]
TRAIN_DIR = "data/train"
VAL_DIR = "data/val"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---- MODEL SETUP ----
print("Loading CLIP model...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)

def extract_embedding(image_path):
    """Extract CLIP embedding for a single image."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
    return embedding.squeeze().cpu().numpy()

def build_dataset(data_dir):
    """Build X, y datasets by extracting embeddings and class labels from a folder."""
    X, y = [], []
    for class_name in CLASSES:
        class_path = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_path):
            continue
        for fname in os.listdir(class_path):
            if not fname.lower().endswith(".jpg"):
                continue
            path = os.path.join(class_path, fname)
            try:
                emb = extract_embedding(path)
                X.append(emb)
                y.append(class_name)
            except Exception as e:
                print(f"Failed to process {path}: {e}")
    return np.array(X), np.array(y)

# ---- DATASET ----
print("Extracting embeddings from training set...")
X_train, y_train = build_dataset(TRAIN_DIR)

print("Extracting embeddings from validation set...")
X_val, y_val = build_dataset(VAL_DIR)

# ---- CLASSIFIER ----
print("Training classifier...")
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# ---- EVALUATION ----
print("\nEvaluating on validation set...")
y_pred = clf.predict(X_val)
print(classification_report(y_val, y_pred, target_names=CLASSES))

# ---- OPTIONAL: Predict on a new image ----
def predict_image(path):
    emb = extract_embedding(path).reshape(1, -1)
    return clf.predict(emb)[0]

# Example use
if __name__ == "__main__":
    test_img = os.path.join(VAL_DIR, "Intacto", os.listdir(os.path.join(VAL_DIR, "Intacto"))[0])
    pred = predict_image(test_img)
    print(f"\nPredicted label for example image: {pred}")