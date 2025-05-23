import os
import sys
import shutil
import json
import asyncio
from collections import OrderedDict
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

# Añadir "src/" al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar desde backend.infer
from backend.infer.mlp_predictor import predict_with_mlp

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

 
# Define upload folder
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


async def get_mapping(task_id: str, file_path: str):
    """
    Process the image and store the classification result.
    Saves response.json in uploads/{task_id}/ when finished.
    """
    print(f"\nProcessing task: {task_id}...")

    try:
       #TO DO: PUT YOU FUNCTION HERE
        # Realizar inferencia Zero-Shot CLIP
        pred_label, score_top1, top3_dict = predict_with_mlp(file_path)

        top_class, score_top1, top3_scores = predict_with_mlp(file_path)

        # Redondear resultados
        score_top1 = round(float(score_top1) * 100, 2)
        top3_scores = {label: round(float(prob), 2) for label, prob in top3_scores.items()}

        # Crear response
        response = {
            "task_id": task_id,
            "status": "Success",
            "response": {
                "Etiqueta": top_class,
                "Probabilidad": f"{score_top1}%",
                "Top 3 resultados": top3_scores,
                "Resultado final": top_class,
                "Comentarios": f"La etiqueta <strong>{top_class}</strong> fue la que obtuvo mejor resultado llegando a <strong>{score_top1}%</strong>"
            },
        }

        response_file = os.path.join(UPLOAD_FOLDER, task_id, "response.json")

# 👇🏽 Aquí agregas el print
        print(f"📁 Guardando response en: {response_file}")

        print(f"Processing succeeded for task {task_id}")

    except Exception as e:
        print(f"Processing failed for task {task_id}: {str(e)}")
        response = {"task_id": task_id, "status": "Failed", "response": None}

    response_file = os.path.join(UPLOAD_FOLDER, task_id, "response.json")
    def convert(o):
        if isinstance(o, np.float32):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    with open(response_file, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, default=convert)


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...), task_id: str = Form()):
    """
    API endpoint to upload an Excel file along with a task_id from the payload.
    """

    print(f"File '{file.filename}' uploaded successfully under task '{task_id}'! Processing...")

    # Ensure the file is an Excel file
    if not file.filename.endswith((".jpg", ".JPG",  ".jpeg", ".JPEG", ".PNG", ".png")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid image.")

    # Create task-specific folder
    task_folder = os.path.join(UPLOAD_FOLDER, task_id)
    os.makedirs(task_folder, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(task_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"\n📂 File '{file.filename}' uploaded successfully under task '{task_id}'! Processing...")

    # Run the pipeline asynchronously
    asyncio.create_task(get_mapping(task_id, file_path))

    return {"status": "success"}

@app.get("/check-status/{task_id}")
async def check_status(task_id: str):
    """
    API Endpoint to check the status of a mapping task.
    Returns:
    - "Pending" if processing is still ongoing.
    - "Failed" if processing failed.
    - "Success" with mapping results if processing is complete.
    """

    task_folder = os.path.join(UPLOAD_FOLDER, task_id)
    response_file = os.path.join(task_folder, "response.json")

    # Case 1: Task folder doesn't exist → "Pending"
    if not os.path.exists(task_folder):
        return {"task_id": task_id, "status": "Pending", "response": None}

    # Case 2: Response file doesn't exist → "Pending"
    if not os.path.exists(response_file):
        return {"task_id": task_id, "status": "Pending", "response": None}

    # Case 3: Response file exists → Check if processing succeeded or failed
    try:
        with open(response_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Empty response file.")
            result = json.loads(content)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Failed to parse response.json for task {task_id}: {e}")
        return {"task_id": task_id, "status": "Failed", "response": None}

    if result.get("status") == "Failed":
        return {"task_id": task_id, "status": "Failed", "response": None}

    return {"task_id": task_id, "status": "Success", "response": result.get("response")}



