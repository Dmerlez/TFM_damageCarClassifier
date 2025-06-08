import os
import sys
import shutil
import json
import asyncio
from collections import OrderedDict
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from datetime import datetime
from PIL import Image
from io import BytesIO

# Añadir "src/" al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar desde backend.infer
from backend.infer.mlp_predictor import predict_with_mlp
now = datetime.now().strftime("%d/%m/%Y - %H:%M")
now1 = datetime.now().strftime("%d/%m/%Y a las %H:%M")
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
    print(f"\nProcessing task: {task_id}...")

    try:
        # Obtener información del archivo
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            file_size_mb = round(len(file_bytes) / (1024 * 1024), 2)
            image = Image.open(BytesIO(file_bytes))
            width, height = image.size

        # Realizar inferencia
        top_class, score_top1, top3_scores = predict_with_mlp(file_path)
        score_top1 = round(float(score_top1) * 100, 2)
        top3_scores = {label: round(float(prob), 2) for label, prob in top3_scores.items()}

        top_scores = sorted(top3_scores.items(), key=lambda x: x[1], reverse=True)
        top1_score = top_scores[0][1]
        top2_score = top_scores[1][1]
        confianza_pct = round((top1_score - top2_score) * 100, 2)
        confianza_label = "Alta" if confianza_pct > 50 else "Media" if confianza_pct > 20 else "Baja"

        # Formatear fecha y hora
        now = datetime.now().strftime("%d/%m/%Y - %H:%M")

        # Crear response
        response = {
            "task_id": task_id,
            "status": "Success",
            "response": {
                "Modelo": "CLIP + MLPClassifier",
                "Etiqueta": top_class,
                "Probabilidad": f"{score_top1}%",
                "Top 3 resultados": top3_scores,
                "Confianza del modelo": f"{confianza_label} (sobre el {confianza_pct}%)",
                "Fecha y hora": now,
                "Imagen": file_name,
                "Tamaño archivo": f"{file_size_mb} MB",
                "Resolución": f"{width} x {height} px",
                "Resumen": f"La imagen <strong>{file_name}</strong> (resolución <strong>{width} x {height} px</strong>, tamaño <strong>{file_size_mb} MB</strong>) fue analizada utilizando el modelo <strong>CLIP (Zero-Shot) + MLPClassifier</strong>, identificando la etiqueta <strong>{top_class}</strong> como la más probable con una confianza de <strong>{score_top1}%</strong>."

            },
        }

        response_file = os.path.join(UPLOAD_FOLDER, task_id, "response.json")
        print(f"📁 Guardando response en: {response_file}")
        print(f"✅ Processing succeeded for task {task_id}")

    except Exception as e:
        print(f"Processing failed for task {task_id}: {str(e)}")
        response = {"task_id": task_id, "status": "Failed", "response": None}

    # Guardar el response como JSON
    response_file = os.path.join(UPLOAD_FOLDER, task_id, "response.json")
    def convert(o):
        if isinstance(o, np.float32):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    with open(response_file, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, default=convert, ensure_ascii=False)

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



