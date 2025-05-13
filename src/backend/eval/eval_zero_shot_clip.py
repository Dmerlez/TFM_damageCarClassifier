# src/eval/eval_zero_shot.py

import os
from sklearn.metrics import classification_report, accuracy_score
from src.backend.infer.infer_zero_shot_clip import classify_image
from src.config import EVAL_CLASSES

VAL_DIR = "data/all"

def main():
    y_true = []
    y_pred = []

    for class_folder in os.listdir(VAL_DIR):
        class_path = os.path.join(VAL_DIR, class_folder)
        if not os.path.isdir(class_path):
            continue

        for img_name in os.listdir(class_path):
            if not img_name.lower().endswith(".jpg"):
                continue

            img_path = os.path.join(class_path, img_name)
            try:
                pred_label, scores = classify_image(img_path)
                y_pred.append(pred_label)
                y_true.append(class_folder)  # Usa nombre exacto de carpeta

                # Debug opcional:
                # print(f"GT: {class_folder} | Pred: {pred_label} | Top score: {max(scores.items(), key=lambda x: x[1])}")

            except Exception as e:
                print(f"Error al procesar {img_path}: {e}")

    print(f"\nAccuracy: {accuracy_score(y_true, y_pred):.4f}\n")
    print(classification_report(y_true, y_pred, labels=EVAL_CLASSES, zero_division=0))

if __name__ == "__main__":
    main()
