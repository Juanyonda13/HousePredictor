#!/bin/bash

set -e

echo "=============================================="
echo "  DESPLIEGUE DE PREDICCION DE CASAS ML"
echo "=============================================="

PROJECT_NAME="prediccion-casas-ml"
SERVER_USER="root"
SERVER_HOST="168.231.71.181"
SERVER_PATH="/root/projects/${PROJECT_NAME}"
SSH_ALIAS="hostinger"

echo ""
echo "1. Preparando archivos para despliegue..."

if [ ! -f "model/modelo_regresion_lineal.pkl" ]; then
    echo "ADVERTENCIA: Modelo no encontrado. Ejecutando analisis estadistico..."
    python3 analisis_estadistico.py
fi

echo ""
echo "2. Conectando al servidor..."
ssh ${SSH_ALIAS} "mkdir -p ${SERVER_PATH}"

echo ""
echo "3. Copiando archivos al servidor..."
rsync -avz --progress \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='venv' \
    ./ ${SSH_ALIAS}:${SERVER_PATH}/

echo ""
echo "4. Desplegando contenedor en el servidor..."
ssh ${SSH_ALIAS} << 'ENDSSH'
cd /root/projects/prediccion-casas-ml

echo "Deteniendo contenedor anterior (si existe)..."
docker compose down 2>/dev/null || true

echo "Construyendo nueva imagen..."
docker compose build --no-cache

echo "Iniciando contenedor..."
docker compose up -d

echo "Esperando a que el servicio esté listo..."
sleep 10

echo ""
echo "Estado del contenedor:"
docker ps | grep prediccion-casas

echo ""
echo "Ultimas lineas del log:"
docker logs prediccion-casas-web --tail 20

ENDSSH

echo ""
echo "=============================================="
echo "  DESPLIEGUE COMPLETADO"
echo "=============================================="
echo ""
echo "Acceso directo: http://168.231.71.181:5000"
echo ""
echo "Para configurar dominio:"
echo "1. Acceder a Nginx Proxy Manager: http://168.231.71.181:8080"
echo "2. Crear nuevo Proxy Host"
echo "3. Domain: prediccion-casas.tu-dominio.com"
echo "4. Forward to: prediccion-casas-web:5000"
echo "5. Habilitar SSL con Let's Encrypt"
echo ""
echo "Ver logs: ssh hostinger 'docker logs -f prediccion-casas-web'"
echo ""

