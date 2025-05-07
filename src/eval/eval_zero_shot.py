# src/eval/eval_zero_shot.py

import os
from sklearn.metrics import classification_report, accuracy_score
from src.infer.infer_zero_shot import classify_image
from src.config import CLASS_MAPPING, EVAL_CLASSES

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
                pred_prompt, _ = classify_image(img_path)
                pred_label = CLASS_MAPPING.get(pred_prompt, "Indeterminado")

                y_pred.append(pred_label)
                y_true.append(class_folder)  # La carpeta representa la clase real

            except Exception as e:
                print(f"Error al procesar {img_path}: {e}")

    print(f"\nAccuracy: {accuracy_score(y_true, y_pred):.4f}\n")
    print(classification_report(y_true, y_pred, labels=EVAL_CLASSES, zero_division=0))

if __name__ == "__main__":
    main()
