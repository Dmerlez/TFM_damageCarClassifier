import os
import sys
import random
from sklearn.metrics import classification_report, accuracy_score

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.infer.infer_chatgpt import classify_image_chatgpt
from src.config import CLASSES

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAL_DIR = os.path.join(PROJECT_ROOT, "data", "val")


def test_chatgpt_infer():
    """
    Runs a ChatGPT Vision classification test on a single randomly selected image
    from a randomly chosen class folder inside `data/val/`.

    Asserts that the predicted label matches the ground truth label (folder name).

    Raises:
        AssertionError: If the folder is missing, contains no JPGs, or prediction fails.
    """
    chosen_class = random.choice(CLASSES)
    class_folder = os.path.join(VAL_DIR, chosen_class)

    print(f"Looking in: {class_folder}")
    assert os.path.isdir(class_folder), f"Folder not found: {class_folder}"

    image_paths = [
        os.path.join(class_folder, f)
        for f in os.listdir(class_folder)
        if f.lower().endswith(".jpg")
    ]

    assert image_paths, f"No .jpg images found in {class_folder}"

    img_path = random.choice(image_paths)
    pred_label = classify_image_chatgpt(img_path)

    print(f"\nImage: {img_path}")
    print(f"True label: {chosen_class} — Predicted label: {pred_label}")

    assert pred_label == chosen_class, f"Prediction mismatch: {pred_label} != {chosen_class}"


def test_chatgpt_eval():
    """
    Evaluates the ChatGPT Vision classifier on all JPG images in the validation set.

    For each image in `data/val/<class>/`, it predicts the class and compares it
    to the ground truth. Prints classification metrics and enforces a minimum accuracy.

    Raises:
        AssertionError: If any expected class folder is missing or if accuracy < 0.4.
    """
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
                print(f"\nImage: {img_path}")
                print(f"True label: {class_name} — Predicted label: {pred_label}")
            except Exception as e:
                print(f"Failed on {img_path}: {e}")

    acc = accuracy_score(y_true, y_pred)
    print(f"\nChatGPT Accuracy: {acc:.4f}")
    print("\n" + classification_report(y_true, y_pred, labels=CLASSES))

    assert acc > 0.4, "Model performance is too low!!!"


if __name__ == "__main__":
    test_chatgpt_infer()
    # test_chatgpt_eval()