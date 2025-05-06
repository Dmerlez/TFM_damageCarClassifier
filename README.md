# Vehicle Damage Detection Project

This project compares three approaches for vehicle damage classification based on images:

1. **YOLO Fine-Tuning** – Trained on custom dataset for multi-class classification:
   - abolladuras (dents)
   - intacto (no damage)
   - rallones (scratches)
   - siniestro (structural damage)

2. **ChatGPT Vision API** – Uses GPT-4 with image input to classify photos via prompting.

3. **Zero-Shot Classification** – Uses open models (e.g., CLIP) to classify images without training.

## Project Structure

<pre lang="markdown">
TFM_damageCarClassifier/
├── data/                  # Contains train/ and val/ folders
├── models/                # YOLO weights, etc.
├── src/
│   ├── preprocess.py      # Data loading and transformations
│   ├── infer_yolo.py
│   ├── infer_chatgpt.py
│   ├── infer_zero_shot.py
│   ├── evaluate.py
│   └── config.py
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