# backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código del backend
COPY . .

# Copia los modelos previamente descargados
COPY models/hf /app/models/hf

# Expone el puerto si usas Uvicorn
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
