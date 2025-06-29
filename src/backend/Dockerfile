# backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema para OpenCV y ultralytics
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Configurar OpenCV para ejecutarse sin GUI
ENV OPENCV_IO_ENABLE_OPENEXR=1
ENV MPLBACKEND=Agg

# Instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código del backend
COPY . .

# Copia todos los modelos (CLIP, MLP, YOLOv8, etc.)
COPY models/ /app/models/

# Expone el puerto si usas Uvicorn
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
