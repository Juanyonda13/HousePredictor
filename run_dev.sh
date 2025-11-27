#!/bin/bash

# Script para ejecutar el servidor de desarrollo con venv

set -e

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: El entorno virtual no existe"
    echo "   Ejecuta primero: ./setup_venv.sh"
    exit 1
fi

# Activar el entorno virtual
source venv/bin/activate

# Verificar si los modelos están entrenados
if [ ! -d "model/artifacts" ] || [ -z "$(ls -A model/artifacts/*.pkl 2>/dev/null)" ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: No se encontraron modelos entrenados"
    echo "   Ejecuta primero: python model/pipelines/analisis_estadistico.py"
    echo ""
    read -p "¿Deseas continuar de todos modos? (s/N): " respuesta
    if [[ ! "$respuesta" =~ ^[Ss]$ ]]; then
        echo "Saliendo..."
        exit 1
    fi
fi

# Ejecutar la aplicación
echo ""
echo "Iniciando servidor de desarrollo..."
echo ""
python app.py

