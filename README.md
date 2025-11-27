# 📊 Sistema de Predicción de Precios de Casas - Análisis Estadístico

Aplicación web desarrollada con Flask para predecir precios de casas utilizando **Regresión Lineal Múltiple (OLS)** con enfoque en **Probabilidad y Estadística Clásica**.

## 📚 Proyecto Académico

**Universidad:** [Tu Universidad]  
**Materia:** Probabilidad y Estadística  
**Enfoque:** Estadística Clásica (NO Machine Learning)  
**Tecnologías:** Python, Flask, statsmodels, scipy, Bootstrap, Leaflet

---

## 🎯 Características

- ✅ **Análisis estadístico completo** (distribuciones, pruebas de hipótesis, intervalos de confianza)
- ✅ **Regresión Lineal Múltiple (OLS)** con inferencia estadística
- ✅ **Teorema de Bayes** y probabilidades condicionales
- ✅ **9 gráficas estadísticas** generadas automáticamente
- ✅ Interfaz web moderna y responsive
- ✅ Mapa interactivo con visualización de propiedades
- ✅ **Intervalos de confianza del 95%** en cada predicción
- ✅ API RESTful con resultados estadísticos

---

## 🏗️ Arquitectura

```
prediccion-casas-ml/
├── app.py                    # Aplicación Flask (servidor web)
├── requirements.txt          # Dependencias de Python
├── model/
│   ├── train.py             # Script de entrenamiento
│   ├── predict.py           # Módulo de predicción
│   ├── modelo_casas.pkl     # Modelo entrenado (generado)
│   └── preprocessor.pkl     # Preprocesador (generado)
├── templates/
│   ├── index.html           # Página principal
│   └── mapa.html            # Mapa interactivo
├── data/
│   └── SaratogaHouses.csv   # Dataset (generado)
└── README.md
```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar/Navegar al proyecto

```bash
cd /home/juanyonda/projects/prediccion-casas-ml
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📊 Uso del Sistema

### 1. Ejecutar Análisis Estadístico Completo (Primera vez)

Antes de usar la aplicación, debes ejecutar el análisis estadístico:

```bash
python3 analisis_estadistico.py
```

**Este script realiza:**
- ✅ Análisis de distribuciones (Normal, Binomial, Poisson)
- ✅ Cálculo de esperanza y varianza
- ✅ Aplicación del Teorema de Bayes
- ✅ Pruebas de hipótesis (t-test, chi-cuadrado)
- ✅ Intervalos de confianza
- ✅ Regresión Lineal Múltiple (OLS)
- ✅ Genera 9 gráficas estadísticas en `graficas_estadisticas/`
- ✅ Entrena y guarda el modelo de regresión lineal

**Salida esperada:**
```
📊 ANÁLISIS ESTADÍSTICO COMPLETO
✅ Distribuciones analizadas
✅ Pruebas de hipótesis ejecutadas  
✅ Modelo de Regresión Lineal entrenado
   R² = 0.6510 (65.10%)
   RMSE = $58,359
✅ 9 gráficas guardadas en graficas_estadisticas/
```

### 2. Iniciar la Aplicación Web

```bash
python app.py
```

**Salida esperada:**
```
🏠 APLICACIÓN WEB DE PREDICCIÓN DE PRECIOS DE CASAS
✅ Modelo cargado correctamente
🌐 Abriendo servidor en: http://127.0.0.1:5000
```

### 3. Abrir en el Navegador

Abre tu navegador y ve a: **http://127.0.0.1:5000**

---

## 🖥️ Funcionalidades de la Aplicación

### Página Principal (/)

1. **Formulario de Predicción**
   - Ingresa 15 características de la casa
   - Características numéricas: metros, antigüedad, dormitorios, etc.
   - Características categóricas: calefacción, desagüe, etc.
   - Botón "Cargar Ejemplo" para datos de prueba

2. **Panel de Estadísticas**
   - Total de casas en el dataset
   - Precio promedio
   - Precio mínimo y máximo
   - Mediana de precios

3. **Resultado de la Predicción**
   - Muestra el precio estimado
   - **Intervalo de Confianza 95%** (rango donde estará el precio real)
   - R² del modelo (% de varianza explicada)
   - Formato: $XXX,XXX

### Mapa Interactivo (/mapa)

- Visualiza 100 casas del dataset
- Marcadores con colores según precio:
  - 🟢 Verde: < $150,000
  - 🟠 Naranja: $150,000 - $250,000
  - 🔴 Rojo: > $250,000
- Click en marcador muestra:
  - Precio
  - Metros totales
  - Dormitorios y baños
  - Antigüedad
  - Características especiales

---

## 📡 API Endpoints

### 1. POST /api/predecir
Predice el precio de una casa

**Request:**
```json
{
  "metros_totales": 2000,
  "antiguedad": 10,
  "precio_terreno": 50000,
  "metros_habitables": 1500,
  "universitarios": 20,
  "dormitorios": 3,
  "chimenea": 1,
  "banyos": 2,
  "habitaciones": 5,
  "calefaccion": "electric",
  "consumo_calefacion": "typical",
  "desague": "public",
  "vistas_lago": "No",
  "nueva_construccion": "No",
  "aire_acondicionado": "No"
}
```

**Response:**
```json
{
  "precio": 185432.50,
  "ic_inferior": 127000.00,
  "ic_superior": 243000.00,
  "modelo": "Regresión Lineal Múltiple (OLS)",
  "r2": 0.6510,
  "error": null
}
```

### 2. GET /api/estadisticas
Obtiene estadísticas del dataset

**Response:**
```json
{
  "total_casas": 1728,
  "precio_promedio": 212354.45,
  "precio_min": 45000.00,
  "precio_max": 775000.00,
  "precio_mediana": 189900.00
}
```

### 3. GET /api/modelo-info
Información del modelo entrenado

**Response:**
```json
{
  "tipo_modelo": "MLPRegressor (Perceptrón Múltiple)",
  "framework": "scikit-learn",
  "parametros": {
    "hidden_layer_sizes": "(20,)",
    "activation": "relu",
    "alpha": 0.01,
    "learning_rate_init": 0.001
  }
}
```

---

## 📊 Modelo Estadístico

### Algoritmo: Regresión Lineal Múltiple (OLS)

**Descripción:**
- Método de Mínimos Cuadrados Ordinarios (Ordinary Least Squares)
- Estimación de coeficientes con inferencia estadística
- Intervalos de confianza para predicciones
- Pruebas de significancia para cada variable (p-valores)
- R² = 0.6510 (explica el 65.10% de la varianza)

### Características de Entrada (15)

**Numéricas:**
1. metros_totales
2. antiguedad
3. precio_terreno
4. metros_habitables
5. universitarios (%)
6. dormitorios
7. chimenea (número)
8. banyos
9. habitaciones

**Categóricas:**
10. calefaccion (electric, hot water/steam, hot air)
11. consumo_calefacion (typical, low, high)
12. desague (public, septic)
13. vistas_lago (Yes, No)
14. nueva_construccion (Yes, No)
15. aire_acondicionado (Yes, No)

### Coeficientes del Modelo (Interpretables)

| Variable | β (Efecto) | p-valor | Significativo |
|----------|------------|---------|---------------|
| tiene_lago | +$119,714 | < 0.001 | ✅ Sí |
| metros_habitables | +$70/m² | < 0.001 | ✅ Sí |
| baños | +$22,800 | < 0.001 | ✅ Sí |
| antiguedad | -$148/año | < 0.01 | ✅ Sí |

### Métricas de Evaluación

- **R²:** 0.6510 (65.10% de varianza explicada)
- **R² Ajustado:** 0.6486
- **RMSE:** $58,359 (error promedio)
- **Intervalos de Confianza:** 95% para cada predicción

---

## 🔬 Dataset: SaratogaHouses

- **Fuente:** GitHub (público)
- **Tamaño:** 1,728 casas
- **Ubicación:** Saratoga Springs, NY, USA
- **Características:** 16 columnas (15 features + 1 target)

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask:** Framework web Python
- **statsmodels:** Regresión lineal e inferencia estadística
- **scipy:** Funciones estadísticas (distribuciones, pruebas)
- **pandas:** Manipulación de datos
- **numpy:** Operaciones numéricas
- **matplotlib & seaborn:** Visualización estadística

### Frontend
- **Bootstrap 5:** Framework CSS
- **Leaflet:** Mapas interactivos
- **Font Awesome:** Iconos
- **JavaScript:** Interactividad

---

## 📖 Cómo Funciona

1. **Entrenamiento:**
   - Carga 1,728 casas del dataset
   - Divide: 80% entrenamiento, 20% prueba
   - Normaliza variables numéricas
   - Binariza variables categóricas
   - Entrena Red Neuronal con búsqueda de hiperparámetros
   - Evalúa el modelo
   - Guarda modelo entrenado

2. **Predicción:**
   - Usuario ingresa características
   - Sistema aplica preprocesamiento idéntico
   - Modelo predice el precio
   - Resultado se muestra formateado

---

## 🎓 Propósito Académico

Este proyecto demuestra **dominio completo** en Probabilidad y Estadística:

### **Conceptos Estadísticos Cubiertos:**
- ✅ **Distribuciones de probabilidad** (Normal, Binomial, Poisson)
- ✅ **Teorema de Bayes** y probabilidades condicionales
- ✅ **Pruebas de hipótesis** (t-test, chi-cuadrado)
- ✅ **Intervalos de confianza**
- ✅ **Variables aleatorias** y funciones de distribución
- ✅ **Esperanza matemática** y varianza poblacional
- ✅ **Regresión lineal múltiple** con inferencia
- ✅ **Análisis de residuos** y validación de supuestos

### **Habilidades Técnicas:**
- ✅ Desarrollo de aplicaciones web (Flask)
- ✅ Visualización estadística profesional
- ✅ Programación científica en Python
- ✅ Documentación técnica completa
- ✅ Diseño de interfaces de usuario

### **Archivos Clave:**
- 📄 `analisis_estadistico.py` - Script con TODO el análisis
- 📄 `README_ESTADISTICA.md` - Documentación teórica completa
- 📊 `graficas_estadisticas/` - 9 gráficas estadísticas profesionales

---

## 🐛 Solución de Problemas

### Modelo no encontrado
```
⚠️ Modelo no encontrado. Ejecuta 'python3 analisis_estadistico.py' primero.
```
**Solución:** Ejecuta el análisis estadístico primero: `python3 analisis_estadistico.py`

### Error de dependencias
```
ModuleNotFoundError: No module named 'flask'
```
**Solución:** Instala dependencias: `pip install -r requirements.txt`

### Puerto ocupado
```
Address already in use
```
**Solución:** Cambia el puerto en `app.py`: `app.run(port=5001)`

---

## 📝 Notas

- El modelo se entrena con datos históricos y puede no reflejar precios actuales
- Las coordenadas en el mapa son aleatorias (dataset original no tiene geolocalización)
- El rendimiento depende de la calidad y cantidad de datos de entrenamiento

---

## 👨‍💻 Autor

**Juan Yonda**  
Proyecto para la materia de Probabilidad Computacional y Estadística

---

## 📄 Licencia

Este proyecto es de uso académico.

---

## 🆘 Soporte

Si tienes problemas, revisa:
1. Este README completo
2. Los comentarios en el código
3. La consola para mensajes de error

---

**¡Buena suerte con tu proyecto! 🚀**

