import os
import sys
import shutil
import json
import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from datetime import datetime
from PIL import Image
from io import BytesIO

# Añadir "src/" al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar funciones de inferencia
from infer.mlp_predictor import predict_with_mlp 
from infer.infer_chatgpt import predict_with_chatgpt
from infer.infer_yolov8 import predict_with_yolov8 

# Initialize FastAPI
app = FastAPI(title="Vehicle Damage Classifier API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define upload folder
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Constantes
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


def get_current_timestamp() -> str:
    """Retorna timestamp formateado para respuestas."""
    return datetime.now().strftime("%d/%m/%Y - %H:%M")


def get_image_info(file_path: str) -> dict:
    """Extrae información básica de la imagen."""
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        file_size_mb = round(len(file_bytes) / (1024 * 1024), 2)
        image = Image.open(BytesIO(file_bytes))
        width, height = image.size
    
    return {
        "file_name": file_name,
        "file_size_mb": file_size_mb,
        "width": width,
        "height": height
    }


def calculate_confidence_metrics(top3_scores: dict) -> tuple:
    """Calcula métricas de confianza basadas en los top 3 scores."""
    top_scores = sorted(top3_scores.items(), key=lambda x: x[1], reverse=True)
    top1_score = top_scores[0][1]
    top2_score = top_scores[1][1] if len(top_scores) > 1 else 0
    
    confianza_pct = round((top1_score - top2_score) * 100, 2)
    confianza_label = "Alta" if confianza_pct > 50 else "Media" if confianza_pct > 20 else "Baja"
    
    return confianza_pct, confianza_label


def save_response_to_file(response: dict, task_id: str) -> None:
    """Guarda la respuesta como archivo JSON."""
    response_file = os.path.join(UPLOAD_FOLDER, task_id, "response.json")
    
    def json_converter(obj):
        """Convierte tipos numpy a tipos JSON serializables."""
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    with open(response_file, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, default=json_converter, ensure_ascii=False)


async def process_image_predictions(file_path: str) -> dict:
    """Ejecuta las predicciones de los tres modelos y retorna resultados consolidados."""
    
    # Obtener información de la imagen
    image_info = get_image_info(file_path)
    
    # Predicción con CLIP + MLP
    mlp_class, mlp_score, mlp_top3 = predict_with_mlp(file_path)
    mlp_score_pct = round(float(mlp_score) * 100, 2)
    mlp_top3_formatted = {label: round(float(prob), 2) for label, prob in mlp_top3.items()}
    
    # Predicción con ChatGPT
    gpt_label, gpt_confidence = predict_with_chatgpt(file_path)
    print(f"GPT Vision - Etiqueta: {gpt_label}, Confianza: {gpt_confidence}")
    
    # Predicción con YOLOv8
    yolo_class, yolo_score, yolo_top3 = predict_with_yolov8(file_path)
    yolo_score_pct = round(float(yolo_score) * 100, 2)
    print(f"YOLOv8 - Etiqueta: {yolo_class}, Confianza: {yolo_score_pct}%")
    
    return {
        "mlp": {"class": mlp_class, "score": mlp_score_pct, "top3": mlp_top3_formatted},
        "gpt": {"class": gpt_label, "confidence": gpt_confidence},
        "yolo": {"class": yolo_class, "score": yolo_score_pct, "top3": yolo_top3},
        "image_info": image_info
    }


async def get_mapping(task_id: str, file_path: str):
    """Procesa la imagen con los tres modelos y guarda los resultados."""
    print(f"\nProcessing task: {task_id}...")

    try:
        # Ejecutar predicciones
        predictions = await process_image_predictions(file_path)
        
        # Crear respuesta estructurada
        response = {
            "task_id": task_id,
            "status": "Success",
            "response": {
                "Modelo 1": "Chat GPT 4 vision",
                "Etiqueta_gpt": predictions["gpt"]["class"],
                "Probabilidad_gpt": predictions["gpt"]["confidence"],
                "Modelo 2": "CLIP + MLPClassifier",
                "Etiqueta": predictions["mlp"]["class"],
                "Probabilidad": f"{predictions['mlp']['score']}%",
                "Modelo 3": "YOLOv8 Classifier",
                "Etiqueta_yolo": predictions["yolo"]["class"],
                "Probabilidad_yolo": f"{predictions['yolo']['score']}%",
                "Fecha y hora": get_current_timestamp(),
                "Imagen": predictions["image_info"]["file_name"],
                "Tamaño archivo": f"{predictions['image_info']['file_size_mb']} MB",
                "Resolución": f"{predictions['image_info']['width']} x {predictions['image_info']['height']} px"
            },
        }
        
        print(f"✅ Processing succeeded for task {task_id}")

    except Exception as e:
        print(f"❌ Processing failed for task {task_id}: {str(e)}")
        response = {"task_id": task_id, "status": "Failed", "response": None}

    # Guardar respuesta
    save_response_to_file(response, task_id)


@app.post("/upload")
async def upload_image(file: UploadFile = File(...), task_id: str = Form()):
    """Endpoint para subir una imagen y procesarla con los modelos."""
    
    print(f"📤 File '{file.filename}' uploaded for task '{task_id}'")

    # Validar tipo de archivo
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Crear carpeta específica para la tarea
    task_folder = os.path.join(UPLOAD_FOLDER, task_id)
    os.makedirs(task_folder, exist_ok=True)

    # Guardar archivo
    file_path = os.path.join(task_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"📂 File saved to: {file_path}")

    # Ejecutar pipeline de forma asíncrona
    asyncio.create_task(get_mapping(task_id, file_path))

    return {"status": "success", "message": "File uploaded and processing started"}


@app.get("/check-status/{task_id}")
async def check_status(task_id: str):
    """Verifica el estado de procesamiento de una tarea."""
    
    task_folder = os.path.join(UPLOAD_FOLDER, task_id)
    response_file = os.path.join(task_folder, "response.json")

    # Verificar si existe la carpeta de la tarea
    if not os.path.exists(task_folder):
        return {"task_id": task_id, "status": "Pending", "response": None}

    # Verificar si existe el archivo de respuesta
    if not os.path.exists(response_file):
        return {"task_id": task_id, "status": "Pending", "response": None}

    # Leer y retornar resultados
    try:
        with open(response_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Empty response file")
            
            result = json.loads(content)
            
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Failed to parse response.json for task {task_id}: {e}")
        return {"task_id": task_id, "status": "Failed", "response": None}

    # Retornar estado según el resultado
    status = result.get("status", "Failed")
    response_data = result.get("response") if status == "Success" else None
    
    return {"task_id": task_id, "status": status, "response": response_data}


@app.post("/confirm/{task_id}")
async def confirm_results(task_id: str):
    """Confirma y guarda permanentemente los resultados de una tarea."""
    
    try:
        task_folder = os.path.join(UPLOAD_FOLDER, task_id)
        response_file = os.path.join(task_folder, "response.json")
        
        # Validar existencia de datos
        if not os.path.exists(task_folder):
            raise HTTPException(status_code=404, detail="Task not found")
            
        if not os.path.exists(response_file):
            raise HTTPException(status_code=404, detail="Task results not found")
        
        # Leer resultados
        with open(response_file, "r", encoding="utf-8") as f:
            result_data = json.load(f)
        
        # Crear carpeta permanente con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        permanent_folder = os.path.join(UPLOAD_FOLDER, f"confirmed_{timestamp}_{task_id}")
        os.makedirs(permanent_folder, exist_ok=True)
        
        # Copiar archivos a carpeta permanente
        for file_name in os.listdir(task_folder):
            source_file = os.path.join(task_folder, file_name)
            dest_file = os.path.join(permanent_folder, file_name)
            shutil.copy2(source_file, dest_file)
        
        # Agregar metadatos de confirmación
        result_data["confirmed_at"] = get_current_timestamp()
        result_data["confirmed_folder"] = permanent_folder
        
        # Guardar resultado confirmado
        confirmed_file = os.path.join(permanent_folder, "confirmed_result.json")
        save_response_to_file(result_data, "confirmed")
        
        print(f"✅ Data confirmed and saved to: {permanent_folder}")
        
        return {
            "status": "success", 
            "message": "Data saved successfully",
            "saved_to": permanent_folder,
            "task_id": task_id
        }
        
    except Exception as e:
        print(f"❌ Error confirming data for task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")