#!/bin/bash

# Script para configurar el entorno virtual del proyecto

set -e

echo "=========================================="
echo "  Configuración del Entorno Virtual"
echo "=========================================="
echo ""

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "   Por favor, instala Python 3.10 o superior"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python encontrado: $(python3 --version)"

# Crear el entorno virtual
if [ -d "venv" ]; then
    echo "⚠️  El entorno virtual 'venv' ya existe"
    read -p "¿Deseas eliminarlo y crear uno nuevo? (s/N): " respuesta
    if [[ "$respuesta" =~ ^[Ss]$ ]]; then
        echo "Eliminando entorno virtual existente..."
        rm -rf venv
    else
        echo "Usando el entorno virtual existente"
    fi
fi

if [ ! -d "venv" ]; then
    echo ""
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
fi

# Activar el entorno virtual
echo ""
echo "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependencias
echo ""
echo "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "  ✅ Configuración completada"
echo "=========================================="
echo ""
echo "Para activar el entorno virtual en el futuro, ejecuta:"
echo "  source venv/bin/activate"
echo ""
echo "Para desactivar el entorno virtual, ejecuta:"
echo "  deactivate"
echo ""

