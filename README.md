# Vehicle Damage Detection Project

Este proyecto compara tres enfoques para la clasificación de daños vehiculares basados en imágenes:

1. **YOLOv8 Fine-Tuning** – Entrenado en dataset personalizado para clasificación multi-clase:
   - Abolladuras (dents)
   - Intacto (no damage)  
   - Rayones (scratches)
   - Siniestro (structural damage)

2. **ChatGPT Vision API** – Usa GPT-4 con entrada de imagen para clasificar fotos mediante prompting.

3. **CLIP + MLP Classifier** – Usa modelos abiertos (CLIP) para clasificar imágenes con pocos ejemplos de entrenamiento.

## 🚀 Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose instalados
- Clave API de OpenAI (para ChatGPT Vision)

### Configuración de Variables de Entorno

1. **Configurar variables de entorno de OpenAI:**

   Copia el archivo de ejemplo y configura tus credenciales:
   ```bash
   cp .env.example .env
   ```
   
   Edita el archivo `.env` con tus credenciales reales de OpenAI:
   ```bash
   OPENAI_API_KEY=sk-proj-tu-clave-api-aqui
   OPENAI_ORG_ID=org-tu-organizacion-id-aqui  
   OPENAI_PROJECT_ID=proj_tu-proyecto-id-aqui
   ```

### Ejecutar con Docker

2. **Construir el contenedor:**
   ```bash
   docker compose build
   ```

3. **Levantar el contenedor:**
   ```bash
   docker compose up
   ```

La aplicación estará disponible en:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 📊 Modelos Incluidos

### YOLOv8 Classifier
- **Modelo entrenado**: `src/backend/models/yolov8_damage_classifier.pt`
- **Accuracy**: 83.6% en dataset de validación
- **Clases**: 4 categorías de daños vehiculares

### ChatGPT Vision API  
- **Modelo**: GPT-4 con capacidades de visión
- **Método**: Clasificación mediante prompting estructurado
- **Entrada**: Imagen + prompt descriptivo

### CLIP + MLP Classifier
- **Embeddings**: CLIP (clip-vit-base-patch32)
- **Clasificador**: Multi-Layer Perceptron entrenado sobre embeddings CLIP
- **Método**: Few-shot learning con representaciones pre-entrenadas

## 🏗️ Estructura del Proyecto

```
TFM_damageCarClassifier/
├── data/                          # Datasets de entrenamiento y validación
├── models/                        # Modelos entrenados (CLIP, encoders, etc.)
├── src/
│   ├── backend/                   # API FastAPI
│   │   ├── api.py                # Endpoint principal
│   │   ├── infer/                # Scripts de inferencia por modelo
│   │   ├── train/                # Scripts de entrenamiento  
│   │   ├── eval/                 # Scripts de evaluación
│   │   └── models/               # Modelos y artefactos entrenados
│   └── frontend/                 # Aplicación React
│       ├── src/components/       # Componentes UI
│       └── public/               # Archivos estáticos
├── tests/                        # Tests automatizados
├── docker-compose.yml            # Configuración Docker
├── .env.example                  # Variables de entorno (template)
└── README.md                     # Este archivo
```

## 🔧 Desarrollo Local (Opcional)

Si prefieres ejecutar sin Docker:

### Backend
```bash
cd src/backend  
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd src/frontend
npm install
npm start
```

## 📈 Evaluación

Los modelos se evalúan usando:
- Accuracy
- Precision  
- Recall
- F1-Score
- Confusion Matrix

## 🧪 Testing

Ejecutar tests automatizados:
```bash
pytest tests/
```

## 📝 Notas Técnicas

- **YOLOv8**: Modelo específico entrenado con transfer learning
- **CLIP**: Embeddings multi-modales pre-entrenados  
- **ChatGPT**: API de OpenAI con capacidades de visión
- **Backend**: FastAPI con endpoints asíncronos
- **Frontend**: React con TypeScript y styled-components

## 🚧 Desarrollo Futuro

- Integración de modelos adicionales (DETR, EfficientDet)
- Mejoras en prompting para ChatGPT
- Optimización de embeddings CLIP  
- Deployment en producción