import os
import numpy as np

# Configuración para entorno headless (Docker)
os.environ['MPLBACKEND'] = 'Agg'  # Matplotlib sin GUI
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'

# Importar después de configurar entorno
from ultralytics import YOLO
from PIL import Image
import torch

# Configuración adicional para ultralytics en Docker
os.environ['YOLO_VERBOSE'] = 'False'

# Carpeta donde está tu script actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta al modelo YOLOv8 entrenado
model_path = os.path.join(BASE_DIR, "..", "models", "yolov8_damage_classifier.pt")

# Clases del modelo YOLOv8 (deben coincidir con las carpetas de entrenamiento)
YOLO_CLASSES = ["Abolladuras", "Intacto", "Rayones", "Siniestro"]

# Variable global para el modelo
yolo_model = None

def load_yolo_model():
    """Carga el modelo YOLOv8 de forma lazy"""
    global yolo_model
    if yolo_model is None:
        if os.path.exists(model_path):
            print(f"Cargando modelo YOLOv8 desde: {model_path}")
            yolo_model = YOLO(model_path)
        else:
            print(f"⚠️  Modelo YOLOv8 no encontrado en {model_path}")
            print("Usando modelo preentrenado yolov8n-cls.pt como fallback")
            yolo_model = YOLO('yolov8n-cls.pt')
    return yolo_model

def predict_with_yolov8(image_path: str):
    """
    Realiza predicción con YOLOv8 siguiendo el mismo patrón que los otros predictors
    
    Args:
        image_path (str): Ruta a la imagen
        
    Returns:
        tuple: (top_class, top_prob, top3_dict)
    """
    try:
        model = load_yolo_model()
        
        # Realizar predicción
        results = model.predict(image_path, imgsz=224, verbose=False)
        
        if not results or len(results) == 0:
            raise ValueError("No se pudieron obtener resultados de YOLOv8")
        
        result = results[0]
        
        # Obtener probabilidades
        if hasattr(result, 'probs') and result.probs is not None:
            probs = result.probs.data.cpu().numpy()
            
            # Si el modelo fue entrenado con nuestros datos, usar nuestras clases
            if len(probs) == len(YOLO_CLASSES):
                classes = YOLO_CLASSES
            else:
                # Fallback: usar las clases del modelo preentrenado
                classes = [f"Clase_{i}" for i in range(len(probs))]
            
            # Obtener top class
            top_idx = np.argmax(probs)
            top_class = classes[top_idx]
            top_prob = float(probs[top_idx])
            
            # Obtener top 3
            top3_idx = np.argsort(probs)[-3:][::-1]
            top3_dict = {classes[i]: float(probs[i]) for i in top3_idx}
            
            return top_class, top_prob, top3_dict
            
        else:
            raise ValueError("El modelo YOLOv8 no devolvió probabilidades válidas")
            
    except Exception as e:
        print(f"Error en predicción YOLOv8: {str(e)}")
        # Retornar valores por defecto en caso de error
        return "Error", 0.0, {"Error": 0.0, "N/A": 0.0, "Unknown": 0.0}

def train_yolov8_model(data_path: str, epochs: int = 50):
    """
    Entrena el modelo YOLOv8 con los datos proporcionados
    
    Args:
        data_path (str): Ruta a la carpeta de datos estructurada
        epochs (int): Número de épocas de entrenamiento
    """
    print(f"Iniciando entrenamiento YOLOv8 con datos en: {data_path}")
    
    # Cargar modelo preentrenado
    model = YOLO('yolov8n-cls.pt')
    
    # Entrenar
    results = model.train(
        data=data_path,
        epochs=epochs,
        imgsz=224,
        batch=16,
        patience=5,
        val=True,
        project=os.path.join(BASE_DIR, "..", "models"),
        name="yolov8_damage_training"
    )
    
    # Guardar el modelo entrenado
    model.save(model_path)
    print(f"✅ Modelo YOLOv8 guardado en: {model_path}")
    
    return results

if __name__ == "__main__":
    # Script para entrenar el modelo si se ejecuta directamente
    import sys
    
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
        train_yolov8_model(data_path)
    else:
        print("Uso: python infer_yolov8.py <ruta_a_datos>")
        print("Ejemplo: python infer_yolov8.py /path/to/damage_dataset") 