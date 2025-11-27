# Predicción de Precios de Casas - ML

Aplicación web para predecir precios de casas utilizando modelos de regresión lineal (OLS) y regresión bayesiana.

## Descripción

Sistema de predicción de precios de viviendas basado en análisis estadístico que combina dos metodologías complementarias:

- **Regresión Lineal Múltiple (OLS)**: Modelo frecuentista que utiliza mínimos cuadrados ordinarios
- **Regresión Bayesiana**: Modelo probabilístico basado en el Teorema de Bayes

El sistema proporciona predicciones con intervalos de confianza/creíbles, análisis paso a paso y comparación entre ambos enfoques estadísticos.

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación

### Configuración del Entorno Virtual

1. Crear y configurar el entorno virtual:

```bash
./setup_venv.sh
```

O manualmente:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Entrenar los modelos:

```bash
source venv/bin/activate
python model/pipelines/analisis_estadistico.py
```

3. Ejecutar la aplicación:

```bash
./run_dev.sh
```

O manualmente:

```bash
source venv/bin/activate
python app.py
```

4. Acceder a la aplicación:

```
http://127.0.0.1:5000
```

## Estructura del Proyecto

```
prediccion-casas-ml/
├── app/                    # Aplicación Flask (MVC)
│   ├── __init__.py        # Factory de la aplicación
│   ├── routes/            # Blueprints de rutas
│   │   ├── api.py         # Endpoints API REST
│   │   └── web.py         # Rutas web (HTML)
│   ├── controllers/        # Controladores (lógica de negocio)
│   │   ├── prediction_controller.py
│   │   └── stats_controller.py
│   ├── services/          # Servicios (lógica de dominio)
│   │   ├── model_service.py
│   │   └── stats_service.py
│   └── common/            # Utilidades comunes
│       ├── config.py      # Configuración centralizada
│       └── decorators.py  # Decoradores (manejo de errores)
│
├── model/                  # Modelos de ML
│   ├── domain/            # Modelos de dominio
│   │   ├── regresion_lineal.py
│   │   ├── regresion_bayesiana.py
│   │   └── analisis_distribuciones.py
│   ├── pipelines/         # Scripts de entrenamiento
│   │   └── analisis_estadistico.py
│   └── artifacts/         # Modelos entrenados (.pkl)
│
├── data/                   # Datos del dataset
│   └── SaratogaHouses.csv
│
├── templates/              # Plantillas HTML
│   ├── index.html
│   ├── analisis_estadistico.html
│   └── mapa.html
│
├── static/                 # Archivos estáticos
│   ├── css/
│   └── js/
│
├── requirements.txt        # Dependencias Python
├── setup_venv.sh          # Script de configuración
├── run_dev.sh             # Script de ejecución
└── check_setup.sh         # Script de verificación
```

## Arquitectura

El proyecto sigue una arquitectura MVC (Model-View-Controller) con las siguientes capas:

- **Routes**: Definen los endpoints (web y API)
- **Controllers**: Orquestan la lógica de negocio
- **Services**: Encapsulan la lógica de dominio
- **Models**: Contienen los modelos de ML y análisis estadístico

## API Endpoints

### Predicción

- `POST /api/predecir`: Predice el precio de una casa
  - Parámetros: `paso_a_paso` (query, opcional): `true` para incluir análisis paso a paso

### Información de Modelos

- `GET /api/status-modelos`: Estado de los modelos cargados
- `GET /api/modelo-info`: Información detallada de los modelos
- `GET /api/datos-ejemplo`: Datos de ejemplo para testing

### Estadísticas

- `GET /api/estadisticas`: Estadísticas descriptivas del dataset
- `GET /api/analisis-estadistico`: Análisis estadístico académico completo

### Comparación

- `POST /api/comparar`: Compara predicciones de múltiples casas

## Rutas Web

- `/`: Página principal con formulario de predicción
- `/mapa`: Mapa interactivo con muestra de casas del dataset
- `/analisis-estadistico`: Análisis estadístico académico detallado

## Modelos Estadísticos

### Regresión Lineal (OLS)

Modelo frecuentista que utiliza mínimos cuadrados ordinarios para estimar los coeficientes. Proporciona:

- Coeficientes interpretables con intervalos de confianza
- Pruebas de significancia estadística
- Inferencia estadística formal
- Intervalos de predicción al 95%

### Regresión Bayesiana

Modelo probabilístico que utiliza el Teorema de Bayes para estimar distribuciones posteriores de los coeficientes. Proporciona:

- Distribuciones previas (priors) y posteriores (posteriors)
- Intervalos creíbles (credible intervals)
- Actualización bayesiana con los datos
- Inferencia probabilística

## Tecnologías Utilizadas

- **Backend**: Flask 3.0
- **Machine Learning**: statsmodels, scipy
- **Análisis de Datos**: pandas, numpy
- **Visualización**: matplotlib, seaborn, folium
- **Frontend**: Bootstrap 5, Leaflet.js

## Comandos Útiles

### Activar el entorno virtual

```bash
source venv/bin/activate
```

### Desactivar el entorno virtual

```bash
deactivate
```

### Verificar configuración del entorno

```bash
./check_setup.sh
```

### Reinstalar dependencias

```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Verificar que los modelos están cargados

```bash
source venv/bin/activate
python -c "from app import create_app; app = create_app(); print('Modelos:', app.extensions['model_service'].has_any_model())"
```

## Docker

### Construcción y ejecución con Docker Compose

```bash
docker-compose up --build
```

### Ejecutar en segundo plano

```bash
docker-compose up -d
```

### Ver logs

```bash
docker logs prediccion-casas-web -f
```

### Detener contenedor

```bash
docker-compose down
```

## Desarrollo

### Estructura de Código

El código está organizado siguiendo principios SOLID:

- **Single Responsibility**: Cada clase tiene una única responsabilidad
- **Open/Closed**: Extensible sin modificar código existente
- **Dependency Inversion**: Dependencias inyectadas a través de servicios

### Manejo de Errores

Los errores de API se manejan centralmente mediante el decorador `@handle_api_errors` que:

- Captura excepciones de tipo `ValueError` (400 Bad Request)
- Captura excepciones de tipo `FileNotFoundError` (404 Not Found)
- Captura excepciones genéricas (500 Internal Server Error)

### Configuración

Todas las rutas y configuraciones están centralizadas en `app/common/config.py`:

- `BASE_DIR`: Directorio raíz del proyecto
- `TEMPLATES_PATH`: Ruta a las plantillas HTML
- `STATIC_PATH`: Ruta a los archivos estáticos
- `DATA_PATH`: Ruta al dataset
- `ARTIFACTS_PATH`: Ruta a los modelos entrenados

## Testing

Para verificar que el entorno está correctamente configurado:

```bash
./check_setup.sh
```

Este script verifica:

- Versión de Python
- Existencia del entorno virtual
- Dependencias instaladas
- Estructura de directorios
- Modelos entrenados
- Dataset disponible

## Despliegue

### Requisitos de Producción

- Python 3.10+
- Servidor web (Nginx recomendado como proxy reverso)
- Docker y Docker Compose (opcional)

### Variables de Entorno

El proyecto utiliza configuración por defecto. Para producción, se recomienda:

- Configurar `SECRET_KEY` en `app/__init__.py`
- Configurar variables de entorno para rutas de datos
- Habilitar logging estructurado

## Licencia

Este proyecto es de uso educativo y académico.

## Autor

Proyecto desarrollado para análisis estadístico y predicción de precios de viviendas.

## Referencias

- Dataset: SaratogaHouses (estadísticas de viviendas en Saratoga)
- Framework: Flask 3.0
- Modelos: statsmodels (OLS y aproximación bayesiana)

