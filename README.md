# Vehicle Damage Detection Project

This project compares three approaches for vehicle damage classification based on images:

1. **YOLO Fine-Tuning** – Trained on custom dataset for multi-class classification:
   - abolladuras (dents)
   - intacto (no damage)
   - rayones (scratches)
   - siniestro (structural damage)

2. **ChatGPT Vision API** – Uses GPT-4 with image input to classify photos via prompting.

3. **Zero-Shot Classification** – Uses open models (e.g., CLIP) to classify images without training.

## Quick Start

Follow these steps to get the project up and running locally:

---

### Start the Backend

1. Navigate to the backend directory:

   ```bash
   cd src/backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the API server:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```
This will launch the FastAPI backend at: http://localhost:8000

### Start the Frontend

### Install npm

**macOS**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install node
```
**Windows**

Download and install Node.js (includes npm)
https://nodejs.org

Then: 
   ```bash
    cd frontend
    npm install (only once)
    npm start
   ```
This will launch the React frontend at: http://localhost:3000


## Project Structure
## TO DO: Actualize this chart!!!

<pre lang="markdown">
TFM_damageCarClassifier/
├── data/                  # Contains train/ and val/ folders
├── models/                # YOLO weights, etc.
├── src/
│   ├── eval/
│   │   ├── eval_yolo.py
│   │   ├── eval_zero_shot.py
│   │   ├── eval_chat_gpt.py
│   ├── infer/
│   │   ├── infer_yolo.py
│   │   ├── infer_zero_shot.py
│   │   ├── infer_chat_gpt.py
│   ├── train/
│   │   ├── train_yolo.py
│   │   ├── train_zero_shot.py
│   └── config.py
│   └── preprocess.py
├── tests/
│   ├── test_chatgpt.py
│   └── test_zero_shot.py
├── run_comparison.py      # Entry point: run all methods and compare
├── requirements.txt
├── .gitignore
└── README.md
</pre>

## Evaluation

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

## Usage

```
pip install -r requirements.txt
python run_comparison.py
```

## Next Steps Zero Shot
### Try another models, for example:
  - https://huggingface.co/Salesforce/blip-image-classifier
  - https://huggingface.co/OFA-Sys/OFA-base

### Refine Class Prompts. 
Zero-shot models like CLIP depend heavily on how you phrase the text labels.
Example:
```
CLASSES = [
    "a car with dents",
    "a car with no visible damage",
    "a car with scratches",
    "a car with structural damage"
]
```
### Ensemble Prompting.
Use multiple descriptions per class and average the logits.
Example:
```
SCRATCHES = ["a scratched car", "a car with scratches", "paint damage on a car"]
```

### Preprocess Images
Focus only on the hood area of the car (if possible), and normalize images:
- Crop to the region of interest
- Resize consistently
- Remove background clutter (optionally)


### Evaluate with Per-Class Metrics
Track precision, recall, and F1 per class. Zero-shot often fails more on “similar” categories (e.g., scratches vs. dents).
Use confusion matrices to guide improvements.

### CLIP hybrid with few-shot training
CLIP is a multi-modal model that maps both images and text into the same embedding space. You can leverage this by:
	1.	Using CLIP to extract a feature vector (embedding) for each image.
	2.	Training a lightweight classifier (like logistic regression or SVM) on those embeddings, using just a small labeled dataset (few-shot).
	3.	During inference, use the same CLIP image encoder + your trained classifier to predict labels.

This bypasses the need for GPU-heavy fine-tuning while still leveraging powerful representations from CLIP.


## Next Steps ChatGPT
###  Implement Best Practices for Prompt Engineering

Crafting effective prompts is crucial for obtaining accurate and relevant responses from the API.

## Next Steps Fine-Tuning YOLOv8
1. **Prepare Dataset**  
   - Convert images into YOLO format: each image needs a `.txt` annotation file with `class_id x_center y_center width height`.
   - Organize into:  
     ```
     data/
       train/
         images/
         labels/
       val/
         images/
         labels/
     ```

2. **Create Data Config File**  
   - Define class names, paths, and number of classes for training.

3. **Select a Pretrained Model**  
   - Use a base model like `yolov8n.pt` or `yolov8s.pt` for transfer learning.

4. **Train the Model**  
   - Use the Ultralytics CLI or Python API to run training with your config and dataset.

5. **Evaluate Performance**  
   - Compare metrics (mAP, precision, recall) with ChatGPT and CLIP classifiers.

6. **Export Model**  
   - Save trained weights and convert to ONNX or other formats if needed.

7. **Integrate into Inference Pipeline**  
   - Use `infer_yolo.py` to run predictions and unify evaluation with other models.


## Try alternatives to YOLO for Vehicle Damage Detection

While YOLOv8 is a strong baseline for object detection, several other models may offer better performance or additional capabilities for subtle or localized damage classification.

### 1. **DETR / DINO / DINOv2**  
- Transformer-based object detectors from Meta.
- Excellent at handling complex scenes and subtle features (scratches, dents).
- Use when damage is irregular or hard to localize.
- [facebook/detr](https://huggingface.co/facebook/detr-resnet-50), [DINOv2 repo](https://github.com/facebookresearch/dinov2)

### 2. **EfficientDet**  
- Lightweight yet accurate object detector from Google.
- Great for mobile or edge deployment.
- Scales well with small or noisy datasets.

### 3. **Mask R-CNN**  
- Detects objects and provides pixel-level segmentation.
- Best choice when damage area (scratch, dent) shape matters.
- Useful for measuring or visualizing affected regions.
- Available in Detectron2 and MMDetection.

### 4. **ConvNeXt (Fine-Tuned Classifier)**  
- A high-performance image classifier based on ConvNet++.
- Ideal for whole-image classification of damage types.
- Simpler and more accurate than YOLO when localization is not needed.
- [facebook/convnext-base-224](https://huggingface.co/facebook/convnext-base-224)

### 5. **Vision Transformers (ViT, Swin, SAM-ViT)**  
- Transformer-based architectures for image classification and segmentation.
- High interpretability and performance.
- Great fit for custom training or as backbones in hybrid detection models.