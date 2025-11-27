#!/bin/bash

# Script de inicio rápido para el proyecto

echo "=============================================="
echo "🏠 Sistema de Predicción de Precios de Casas"
echo "=============================================="
echo ""

# Verificar si existe el modelo
if [ ! -f "model/modelo_casas.pkl" ]; then
    echo "⚠️  Modelo no encontrado"
    echo "📊 Iniciando entrenamiento del modelo..."
    echo ""
    python3 model/train.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Modelo entrenado exitosamente"
    else
        echo ""
        echo "❌ Error en el entrenamiento"
        exit 1
    fi
else
    echo "✅ Modelo encontrado"
fi

echo ""
echo "🚀 Iniciando aplicación web..."
echo ""
python3 app.py

