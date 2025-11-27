#!/bin/bash

# Script de inicio rápido para el proyecto

echo "=============================================="
echo "🏠 Sistema de Predicción de Precios de Casas"
echo "=============================================="
echo ""

# Verificar si existen los modelos estadísticos (OLS y Bayesiano)
OLS_MODEL="model/modelo_regresion_lineal.pkl"
BAYES_MODEL="model/modelo_regresion_bayesiana.pkl"

if [ ! -f "$OLS_MODEL" ] || [ ! -f "$BAYES_MODEL" ]; then
    echo "⚠️  Modelos estadísticos no encontrados"
    echo "📊 Ejecutando análisis estadístico completo..."
    echo ""
    python3 analisis_estadistico.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Modelos entrenados y análisis completado"
    else
        echo ""
        echo "❌ Error en el análisis estadístico"
        exit 1
    fi
else
    echo "✅ Modelos estadísticos encontrados"
fi

echo ""
echo "🚀 Iniciando aplicación web..."
echo ""
python3 app.py

