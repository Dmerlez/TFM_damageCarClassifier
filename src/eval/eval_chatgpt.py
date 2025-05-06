import os
from src.infer.infer_chatgpt import classify_image_chatgpt
from src.config import CLASSES
from sklearn.metrics import classification_report, accuracy_score

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VAL_DIR = os.path.join(PROJECT_ROOT, "data", "val")

def evaluate_chatgpt():
    y_true, y_pred = [], []

    for class_name in CLASSES:
        class_path = os.path.join(VAL_DIR, class_name)
        assert os.path.isdir(class_path), f"Missing folder: {class_path}"

        for fname in os.listdir(class_path):
            if not fname.lower().endswith(".jpg"):
                continue

            img_path = os.path.join(class_path, fname)

            try:
                pred_label = classify_image_chatgpt(img_path)
                y_true.append(class_name)
                y_pred.append(pred_label)
                print(f"{fname} | True: {class_name} | Pred: {pred_label}")
            except Exception as e:
                print(f"Failed on {img_path}: {e}")

    print("\n--- Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print(classification_report(y_true, y_pred, labels=CLASSES))