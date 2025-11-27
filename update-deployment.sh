#!/bin/bash

set -e

echo "=============================================="
echo "  ACTUALIZACION RAPIDA - PREDICCION CASAS ML"
echo "=============================================="

SSH_ALIAS="hostinger"
SERVER_PATH="/root/projects/prediccion-casas-ml"

echo ""
echo "1. Copiando archivos actualizados..."
rsync -avz --progress \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='venv' \
    ./ ${SSH_ALIAS}:${SERVER_PATH}/

echo ""
echo "2. Reconstruyendo y actualizando contenedor..."
ssh ${SSH_ALIAS} << 'ENDSSH'
cd /root/projects/prediccion-casas-ml

echo "Deteniendo contenedor anterior..."
docker compose down

echo ""
echo "Reconstruyendo imagen con los nuevos cambios..."
docker compose build --no-cache

echo ""
echo "Iniciando contenedor con la nueva imagen..."
docker compose up -d

echo ""
echo "Esperando a que el servicio este listo..."
sleep 10

echo ""
echo "Estado del contenedor:"
docker ps | grep prediccion-casas

echo ""
echo "Ultimas lineas del log:"
docker logs prediccion-casas-web --tail 20

echo ""
echo "Verificando salud del contenedor..."
sleep 5
docker inspect --format='{{.State.Health.Status}}' prediccion-casas-web 2>/dev/null || echo "Health check en progreso..."

ENDSSH

echo ""
echo "=============================================="
echo "  ACTUALIZACION COMPLETADA"
echo "=============================================="
echo ""
echo "Acceso: http://168.231.71.181:5000"
echo "Logs: ssh hostinger 'docker logs -f prediccion-casas-web'"
echo ""

