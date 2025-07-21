"""
Módulo de inferencia para YOLOv8 en clasificación de daños vehiculares.
"""
import numpy as np
from ultralytics import YOLO
from PIL import Image
import torch
from typing import Tuple, Dict, Optional

# Importar utilidades comunes
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import setup_environment_for_docker, get_model_path, validate_image_path, logger

# Configurar entorno para Docker
setup_environment_for_docker()

# Configuración del modelo
MODEL_FILENAME = "yolov8_damage_classifier.pt"
FALLBACK_MODEL = "yolov8n-cls.pt"
YOLO_CLASSES = ["Abolladuras", "Intacto", "Rayones", "Siniestro"]

# Variable global para el modelo (lazy loading)
yolo_model: Optional[YOLO] = None


def load_yolo_model() -> YOLO:
    """Carga el modelo YOLOv8 de forma lazy con fallback automático."""
    global yolo_model
    
    if yolo_model is None:
        model_path = get_model_path(MODEL_FILENAME)
        
        if model_path.exists():
            logger.info(f"Cargando modelo YOLOv8 desde: {model_path}")
            yolo_model = YOLO(str(model_path))
        else:
            logger.warning(f"⚠️  Modelo YOLOv8 no encontrado en {model_path}")
            logger.info(f"Usando modelo preentrenado {FALLBACK_MODEL} como fallback")
            yolo_model = YOLO(FALLBACK_MODEL)
    
    return yolo_model


def predict_with_yolov8(image_path: str) -> Tuple[str, float, Dict[str, float]]:
    """
    Realiza predicción con YOLOv8 para clasificación de daños vehiculares.
    
    Args:
        image_path (str): Ruta a la imagen
        
    Returns:
        tuple: (clase_principal, probabilidad_principal, diccionario_top3)
        
    Raises:
        ValueError: Si la imagen no es válida
        RuntimeError: Si hay error en la predicción
    """
    # Validar imagen
    if not validate_image_path(image_path):
        raise ValueError(f"Imagen no válida o no encontrada: {image_path}")
    
    try:
        # Cargar modelo
        model = load_yolo_model()
        
        # Realizar predicción
        results = model(image_path, verbose=False)
        
        if not results or len(results) == 0:
            raise RuntimeError("No se obtuvieron resultados de la predicción")
        
        # Extraer probabilidades
        result = results[0]
        probs = result.probs
        
        if probs is None:
            raise RuntimeError("No se pudieron extraer probabilidades del resultado")
        
        # Obtener índices y probabilidades ordenadas
        top_indices = probs.top5
        top_confidences = probs.top5conf.cpu().numpy()
        
        # Crear diccionario con top 3 resultados
        top3_dict = {}
        for i in range(min(3, len(top_indices))):
            class_idx = top_indices[i]
            if class_idx < len(YOLO_CLASSES):
                class_name = YOLO_CLASSES[class_idx]
                confidence = float(top_confidences[i])
                top3_dict[class_name] = confidence
        
        # Obtener resultado principal
        if top3_dict:
            top_class = next(iter(top3_dict))
            top_confidence = top3_dict[top_class]
        else:
            # Fallback si no hay resultados válidos
            top_class = "Indeterminado"
            top_confidence = 0.0
            top3_dict = {"Indeterminado": 0.0}
        
        logger.info(f"YOLOv8 prediction: {top_class} ({top_confidence:.2%})")
        
        return top_class, top_confidence, top3_dict
        
    except Exception as e:
        logger.error(f"Error en predicción YOLOv8 para {image_path}: {str(e)}")
        raise RuntimeError(f"Error en predicción YOLOv8: {str(e)}")


def get_model_info() -> Dict[str, str]:
    """Retorna información sobre el modelo YOLOv8 cargado."""
    model = load_yolo_model()
    model_path = get_model_path(MODEL_FILENAME)
    
    return {
        "model_type": "YOLOv8 Classifier",
        "model_path": str(model_path) if model_path.exists() else FALLBACK_MODEL,
        "classes": YOLO_CLASSES,
        "status": "loaded" if yolo_model is not None else "not_loaded"
    }


# Funciones de compatibilidad con código existente (para migración gradual)
def train_yolov8_model(data_path: str, epochs: int = 50):
    """
    Entrena el modelo YOLOv8 con los datos proporcionados.
    
    Args:
        data_path (str): Ruta a la carpeta de datos estructurada
        epochs (int): Número de épocas de entrenamiento
    """
    logger.info(f"Iniciando entrenamiento YOLOv8 con datos en: {data_path}")
    
    # Cargar modelo preentrenado
    model = YOLO('yolov8n-cls.pt')
    
    # Configurar ruta de salida
    models_dir = get_model_path("").parent
    
    # Entrenar
    results = model.train(
        data=data_path,
        epochs=epochs,
        imgsz=224,
        batch=16,
        patience=5,
        val=True,
        project=str(models_dir),
        name="yolov8_damage_training"
    )
    
    # Guardar el modelo entrenado
    save_path = get_model_path(MODEL_FILENAME)
    model.save(str(save_path))
    logger.info(f"✅ Modelo YOLOv8 guardado en: {save_path}")
    
    return results 