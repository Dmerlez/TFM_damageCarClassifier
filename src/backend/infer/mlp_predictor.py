"""
Módulo de inferencia para MLP + CLIP en clasificación de daños vehiculares.
"""
import torch
import numpy as np
import joblib
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from scipy.special import softmax
from typing import Tuple, Dict
import sys
import os

# Importar utilidades comunes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_models_dir, validate_image_path, safe_float_conversion, logger

# Configuración de modelos
MODEL_FILES = {
    "mlp": "MLPClassifier_clip_model.pkl",
    "scaler": "MLPClassifier_scaler.pkl", 
    "encoder": "MLPClassifier_label_encoder.pkl"
}

CLIP_MODEL_LOCAL_PATH = "hf/clip-vit-base-patch32"
CLIP_MODEL_REMOTE = "openai/clip-vit-base-patch32"

# Variables globales para lazy loading
clip_model = None
clip_processor = None
mlp_model = None
scaler = None
label_encoder = None
classes = None


def load_clip_model():
    """Carga el modelo CLIP con fallback automático."""
    global clip_model, clip_processor
    
    if clip_model is None:
        models_dir = get_models_dir()
        clip_model_path = models_dir / CLIP_MODEL_LOCAL_PATH
        
        # Intentar cargar desde directorio local
        try:
            clip_model = CLIPModel.from_pretrained(
                str(clip_model_path),
                local_files_only=True
            )
            clip_processor = CLIPProcessor.from_pretrained(
                str(clip_model_path),
                local_files_only=True
            )
            logger.info(f"✅ Modelo CLIP cargado desde directorio local: {clip_model_path}")
            
        except (OSError, FileNotFoundError):
            logger.warning(f"⚠️  Modelo CLIP no encontrado localmente en {clip_model_path}")
            logger.info("📥 Descargando modelo CLIP desde Hugging Face...")
            
            clip_model = CLIPModel.from_pretrained(CLIP_MODEL_REMOTE)
            clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_REMOTE)
            logger.info("✅ Modelo CLIP descargado exitosamente desde Hugging Face")
        
        clip_model.eval()
    
    return clip_model, clip_processor


def load_mlp_components():
    """Carga los componentes del modelo MLP (modelo, scaler, encoder)."""
    global mlp_model, scaler, label_encoder, classes
    
    if mlp_model is None:
        models_dir = get_models_dir()
        
        try:
            # Cargar modelo MLP
            mlp_path = models_dir / MODEL_FILES["mlp"]
            mlp_model = joblib.load(str(mlp_path))
            
            # Cargar scaler
            scaler_path = models_dir / MODEL_FILES["scaler"]
            scaler = joblib.load(str(scaler_path))
            
            # Cargar encoder y obtener clases
            encoder_path = models_dir / MODEL_FILES["encoder"]
            label_encoder = joblib.load(str(encoder_path))
            classes = list(label_encoder.classes_)
            
            logger.info("✅ Componentes MLP cargados correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error cargando componentes MLP: {str(e)}")
            raise RuntimeError(f"No se pudieron cargar los modelos MLP: {str(e)}")
    
    return mlp_model, scaler, label_encoder, classes


def extract_clip_features(image_path: str) -> np.ndarray:
    """
    Extrae características CLIP de una imagen.
    
    Args:
        image_path (str): Ruta a la imagen
        
    Returns:
        np.ndarray: Vector de características normalizadas
    """
    # Validar imagen
    if not validate_image_path(image_path):
        raise ValueError(f"Imagen no válida o no encontrada: {image_path}")
    
    # Cargar modelos CLIP
    model, processor = load_clip_model()
    
    try:
        # Procesar imagen
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        
        # Extraer características
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            # Normalizar características
            image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        
        return image_features.cpu().numpy().flatten()
        
    except Exception as e:
        logger.error(f"Error extrayendo características CLIP: {str(e)}")
        raise RuntimeError(f"Error procesando imagen con CLIP: {str(e)}")


def predict_with_mlp(image_path: str) -> Tuple[str, float, Dict[str, float]]:
    """
    Realiza predicción usando MLP + CLIP para clasificación de daños vehiculares.
    
    Args:
        image_path (str): Ruta a la imagen
        
    Returns:
        tuple: (clase_principal, probabilidad_principal, diccionario_top3)
    """
    try:
        # Cargar componentes del modelo
        mlp, scaler_model, encoder, class_names = load_mlp_components()
        
        # Extraer características CLIP
        features = extract_clip_features(image_path)
        
        # Escalar características
        features_scaled = scaler_model.transform(features.reshape(1, -1))
        
        # Realizar predicción
        probabilities = mlp.predict_proba(features_scaled)[0]
        
        # Obtener clase principal
        top_idx = np.argmax(probabilities)
        top_class = class_names[top_idx]
        top_probability = safe_float_conversion(probabilities[top_idx])
        
        # Obtener top 3 resultados
        top3_indices = probabilities.argsort()[-3:][::-1]
        top3_dict = {
            class_names[i]: safe_float_conversion(probabilities[i]) 
            for i in top3_indices
        }
        
        logger.info(f"MLP prediction: {top_class} ({top_probability:.2%})")
        
        return top_class, top_probability, top3_dict
        
    except Exception as e:
        logger.error(f"Error en predicción MLP para {image_path}: {str(e)}")
        raise RuntimeError(f"Error en predicción MLP: {str(e)}")


def get_model_info() -> Dict[str, any]:
    """Retorna información sobre los modelos cargados."""
    try:
        # Intentar cargar componentes para verificar estado
        load_clip_model()
        load_mlp_components()
        
        models_dir = get_models_dir()
        
        return {
            "model_type": "CLIP + MLP Classifier",
            "clip_model": CLIP_MODEL_REMOTE,
            "mlp_model_path": str(models_dir / MODEL_FILES["mlp"]),
            "scaler_path": str(models_dir / MODEL_FILES["scaler"]),
            "encoder_path": str(models_dir / MODEL_FILES["encoder"]),
            "classes": classes if classes else [],
            "status": "loaded" if all([clip_model, mlp_model, scaler, label_encoder]) else "partial"
        }
        
    except Exception as e:
        return {
            "model_type": "CLIP + MLP Classifier",
            "status": "error",
            "error": str(e)
        }
