import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.infer.infer_zero_shot import classify_image
from sklearn.metrics import classification_report, accuracy_score
from src.config import CLASSES

VAL_DIR = "data/val"

y_true = []
y_pred = []

# Traverse class folders
for class_folder in os.listdir(VAL_DIR):
    class_path = os.path.join(VAL_DIR, class_folder)
    if not os.path.isdir(class_path):
        continue

    for img_name in os.listdir(class_path):
        if not img_name.lower().endswith(".jpg"):
            continue

        img_path = os.path.join(class_path, img_name)
        try:
            pred_label, _ = classify_image(img_path)
            y_pred.append(pred_label)
            y_true.append(class_folder)  # Folder = ground truth label
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

# Evaluate predictions
print(f"\nAccuracy: {accuracy_score(y_true, y_pred):.4f}\n")
print(classification_report(y_true, y_pred, labels=CLASSES))