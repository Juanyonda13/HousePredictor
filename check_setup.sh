#!/bin/bash

# Script para verificar que el entorno está correctamente configurado

echo "=========================================="
echo "  Verificación del Entorno"
echo "=========================================="
echo ""

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python: $PYTHON_VERSION"
else
    echo "❌ Python 3 no encontrado"
    exit 1
fi

# Verificar venv
if [ -d "venv" ]; then
    echo "✓ Entorno virtual encontrado"
    
    # Verificar si está activado
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "✓ Entorno virtual activado: $VIRTUAL_ENV"
    else
        echo "⚠️  Entorno virtual no activado (ejecuta: source venv/bin/activate)"
    fi
else
    echo "⚠️  Entorno virtual no encontrado (ejecuta: ./setup_venv.sh)"
fi

# Verificar dependencias
if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt encontrado"
    
    if [ -n "$VIRTUAL_ENV" ]; then
        echo ""
        echo "Verificando dependencias instaladas..."
        MISSING=0
        while IFS= read -r line; do
            if [[ ! "$line" =~ ^#.*$ ]] && [[ ! -z "$line" ]]; then
                PACKAGE=$(echo "$line" | cut -d'=' -f1 | cut -d'<' -f1 | cut -d'>' -f1)
                if ! pip show "$PACKAGE" &> /dev/null; then
                    echo "  ❌ $PACKAGE no instalado"
                    MISSING=1
                fi
            fi
        done < requirements.txt
        
        if [ $MISSING -eq 0 ]; then
            echo "✓ Todas las dependencias están instaladas"
        else
            echo ""
            echo "⚠️  Ejecuta: pip install -r requirements.txt"
        fi
    fi
else
    echo "❌ requirements.txt no encontrado"
fi

# Verificar estructura de directorios
echo ""
echo "Verificando estructura del proyecto..."
REQUIRED_DIRS=("app" "model" "templates" "static" "data")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir/ existe"
    else
        echo "❌ $dir/ no existe"
    fi
done

# Verificar modelos
echo ""
if [ -d "model/artifacts" ] && [ -n "$(ls -A model/artifacts/*.pkl 2>/dev/null)" ]; then
    echo "✓ Modelos entrenados encontrados"
    ls -1 model/artifacts/*.pkl 2>/dev/null | wc -l | xargs echo "  Cantidad de modelos:"
else
    echo "⚠️  Modelos no encontrados (ejecuta: python model/pipelines/analisis_estadistico.py)"
fi

# Verificar datos
if [ -f "data/SaratogaHouses.csv" ]; then
    echo "✓ Dataset encontrado"
else
    echo "⚠️  Dataset no encontrado (data/SaratogaHouses.csv)"
fi

echo ""
echo "=========================================="

