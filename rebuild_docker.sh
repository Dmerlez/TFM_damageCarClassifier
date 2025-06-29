#!/bin/bash

echo "🐳 Reconstruyendo contenedores Docker con soporte para YOLOv8..."
echo "================================================================"

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Limpiar imágenes anteriores (opcional)
echo "🧹 Limpiando imágenes anteriores..."
docker-compose build --no-cache

# Reconstruir e iniciar contenedores
echo "🚀 Reconstruyendo e iniciando contenedores..."
docker-compose up --build -d

# Mostrar logs del backend para verificar
echo "📋 Mostrando logs del backend..."
docker-compose logs backend

echo "✅ ¡Contenedores reconstruidos!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo ""
echo "Para ver logs en tiempo real:"
echo "docker-compose logs -f backend" 