#!/usr/bin/env python3
"""
Script para entrenar YOLOv8 para clasificación de daños en vehículos
Basado en el notebook YOLOV8.ipynb proporcionado
"""

import os
import sys
import shutil
import random
from pathlib import Path
from ultralytics import YOLO

# Añadir src al path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def prepare_yolo_dataset(origen_path: str, destino_path: str, train_ratio: float = 0.8):
    """
    Prepara los datos en el formato que espera YOLOv8 para clasificación
    
    Args:
        origen_path: Ruta a la carpeta con las clases organizadas
        destino_path: Ruta donde guardar el dataset preparado
        train_ratio: Ratio de división train/val
    """
    print(f"📂 Preparando dataset desde: {origen_path}")
    print(f"📁 Destino: {destino_path}")
    
    # Limpiar destino si existe
    if os.path.exists(destino_path):
        shutil.rmtree(destino_path)
    
    # Obtener clases (carpetas)
    if not os.path.exists(origen_path):
        raise FileNotFoundError(f"No se encontró la carpeta de datos: {origen_path}")
    
    clases = [d for d in os.listdir(origen_path) if os.path.isdir(os.path.join(origen_path, d))]
    
    if not clases:
        raise ValueError(f"No se encontraron carpetas de clases en: {origen_path}")
    
    print(f"🏷️  Clases encontradas: {clases}")
    
    # Procesar cada clase
    total_train = 0
    total_val = 0
    
    for clase in clases:
        clase_path = os.path.join(origen_path, clase)
        
        # Obtener todas las imágenes de la clase
        img_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        img_paths = []
        for ext in img_extensions:
            img_paths.extend(list(Path(clase_path).glob(ext)))
        
        if not img_paths:
            print(f"⚠️  No se encontraron imágenes en {clase_path}")
            continue
        
        # Mezclar aleatoriamente
        random.shuffle(img_paths)
        
        # Dividir en train/val
        split_idx = int(len(img_paths) * train_ratio)
        train_imgs = img_paths[:split_idx]
        val_imgs = img_paths[split_idx:]
        
        # Crear carpetas de destino
        for fase, imgs in zip(['train', 'val'], [train_imgs, val_imgs]):
            destino_clase = os.path.join(destino_path, fase, clase)
            os.makedirs(destino_clase, exist_ok=True)
            
            # Copiar imágenes
            for img in imgs:
                shutil.copy2(str(img), os.path.join(destino_clase, img.name))
        
        total_train += len(train_imgs)
        total_val += len(val_imgs)
        
        print(f"✅ {clase}: {len(train_imgs)} train / {len(val_imgs)} val")
    
    print(f"📊 Total: {total_train} train / {total_val} val")
    return destino_path

def train_yolov8_classifier(dataset_path: str, epochs: int = 50, batch_size: int = 16):
    """
    Entrena el clasificador YOLOv8
    
    Args:
        dataset_path: Ruta al dataset preparado
        epochs: Número de épocas
        batch_size: Tamaño del batch
    """
    print(f"🚀 Iniciando entrenamiento YOLOv8...")
    print(f"Dataset: {dataset_path}")
    print(f"Épocas: {epochs}")
    print(f"Batch size: {batch_size}")
    
    # Verificar que el dataset existe
    train_path = os.path.join(dataset_path, 'train')
    val_path = os.path.join(dataset_path, 'val')
    
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"No se encontró carpeta train: {train_path}")
    if not os.path.exists(val_path):
        raise FileNotFoundError(f"No se encontró carpeta val: {val_path}")
    
    # Cargar modelo preentrenado
    model = YOLO('yolov8n-cls.pt')
    
    # Configurar ruta de salida
    project_path = os.path.join(os.path.dirname(__file__), "..", "models")
    
    # Entrenar
    print("🔥 Comenzando entrenamiento...")
    results = model.train(
        data=dataset_path,
        epochs=epochs,
        imgsz=224,
        batch=batch_size,
        patience=5,  # early stopping
        val=True,
        project=project_path,
        name="yolov8_damage_classifier",
        save=True,
        plots=True
    )
    
    # Guardar modelo final con nombre específico
    model_save_path = os.path.join(project_path, "yolov8_damage_classifier.pt")
    model.save(model_save_path)
    
    print(f"✅ Entrenamiento completado!")
    print(f"📦 Modelo guardado en: {model_save_path}")
    
    return results, model_save_path

def evaluate_model(model_path: str, val_dataset_path: str):
    """
    Evalúa el modelo entrenado
    
    Args:
        model_path: Ruta al modelo entrenado
        val_dataset_path: Ruta al dataset de validación
    """
    print(f"📊 Evaluando modelo: {model_path}")
    
    # Cargar modelo
    model = YOLO(model_path)
    
    # Evaluar
    results = model.val(data=val_dataset_path)
    
    print("✅ Evaluación completada")
    return results

def main():
    """Función principal para entrenar YOLOv8"""
    
    # Configuración de rutas
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.join(BASE_DIR, "..", "..", "..")
    
    # Ruta a los datos originales
    data_origen = "/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/data/all"
    
    # Ruta para el dataset preparado
    dataset_destino = os.path.join(PROJECT_ROOT, "data", "yolov8_dataset")
    
    print("=" * 60)
    print("🚗 ENTRENAMIENTO YOLOV8 - CLASIFICADOR DAÑOS VEHICULARES")
    print("=" * 60)
    
    try:
        # Paso 1: Preparar dataset
        print("\n📋 PASO 1: Preparando dataset...")
        prepare_yolo_dataset(data_origen, dataset_destino)
        
        # Paso 2: Entrenar modelo
        print("\n🎯 PASO 2: Entrenando modelo...")
        results, model_path = train_yolov8_classifier(dataset_destino, epochs=50)
        
        # Paso 3: Evaluar modelo
        print("\n📈 PASO 3: Evaluando modelo...")
        evaluate_model(model_path, dataset_destino)
        
        print("\n" + "=" * 60)
        print("🎉 ¡ENTRENAMIENTO COMPLETADO EXITOSAMENTE!")
        print(f"📦 Modelo disponible en: {model_path}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Configurar semilla para reproducibilidad
    random.seed(42)
    
    # Ejecutar entrenamiento
    main() 