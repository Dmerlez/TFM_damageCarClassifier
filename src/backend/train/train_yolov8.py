#!/usr/bin/env python3
"""
Script simple para entrenar YOLOv8 en la clasificación de daños vehiculares
Uso: python train_yolov8.py
"""

import os
import sys

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.backend.train.train_yolov8_classifier import main as train_main

if __name__ == "__main__":
    print("🚗 Iniciando entrenamiento YOLOv8 para clasificación de daños vehiculares")
    print("-" * 70)
    print("Este script:")
    print("1. Preparará los datos desde la carpeta 'data'")
    print("2. Dividirá en train/validation (80/20)")
    print("3. Entrenará YOLOv8 por 50 épocas con early stopping")
    print("4. Guardará el modelo entrenado en 'src/backend/models/'")
    print("-" * 70)
    
    # Verificar que existe la carpeta de datos
    data_path = "/Users/davidmerlez/Desktop/Master UIC/TFM/github/TFM_damageCarClassifier/data/all"
    if not os.path.exists(data_path):
        print(f"❌ No se encontró la carpeta de datos: {data_path}")
        print("Por favor, asegúrate de que los datos estén organizados en carpetas por clase")
        sys.exit(1)
    
    # Mostrar clases encontradas
    clases = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    if clases:
        print(f"📁 Clases encontradas: {', '.join(clases)}")
    else:
        print("❌ No se encontraron carpetas de clases en los datos")
        sys.exit(1)
        
    response = input("\n¿Deseas continuar con el entrenamiento? (s/n): ")
    if response.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Entrenamiento cancelado.")
        sys.exit(0)
    
    try:
        train_main()
    except KeyboardInterrupt:
        print("\n🛑 Entrenamiento interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")
        sys.exit(1) 