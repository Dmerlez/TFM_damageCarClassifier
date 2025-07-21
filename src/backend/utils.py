"""
Utilidades comunes para el backend del clasificador de daños vehiculares.
"""
import os
from pathlib import Path
from typing import Dict, Any
import logging

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Retorna la ruta raíz del proyecto."""
    return Path(__file__).resolve().parent.parent.parent


def get_backend_root() -> Path:
    """Retorna la ruta raíz del backend."""
    return Path(__file__).resolve().parent


def get_models_dir() -> Path:
    """Retorna la ruta al directorio de modelos."""
    return get_backend_root() / "models"


def get_data_dir() -> Path:
    """Retorna la ruta al directorio de datos."""
    return get_project_root() / "data"


def setup_environment_for_docker():
    """Configura variables de entorno para ejecutar en Docker sin GUI."""
    os.environ['MPLBACKEND'] = 'Agg'  # Matplotlib sin GUI
    os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
    os.environ['YOLO_VERBOSE'] = 'False'


def validate_image_path(image_path: str) -> bool:
    """Valida que el archivo de imagen existe y tiene extensión válida."""
    if not os.path.exists(image_path):
        return False
    
    valid_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    file_extension = os.path.splitext(image_path)[1]
    
    return file_extension in valid_extensions


def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """Convierte un valor a float de forma segura."""
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.warning(f"No se pudo convertir {value} a float, usando {default}")
        return default


def format_confidence_percentage(confidence: float) -> str:
    """Formatea la confianza como porcentaje con 2 decimales."""
    return f"{round(confidence * 100, 2)}%"


def get_model_path(model_name: str) -> Path:
    """Retorna la ruta completa a un modelo específico."""
    models_dir = get_models_dir()
    return models_dir / model_name


def ensure_directory_exists(directory_path: str) -> None:
    """Crea un directorio si no existe."""
    os.makedirs(directory_path, exist_ok=True) 