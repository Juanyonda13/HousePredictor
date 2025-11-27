# Diagrama de Desarrollo del Proyecto

Diagrama explicativo del desarrollo y arquitectura del sistema de predicción de precios de casas para exposición académica.

```mermaid
flowchart TB
    subgraph Fase1["FASE 1: PREPARACION DE DATOS"]
        A[Dataset SaratogaHouses.csv] --> B[Análisis Exploratorio]
        B --> C[Preprocesamiento de Datos]
        C --> D[Creación Variables Dummy]
    end
    
    subgraph Fase2["FASE 2: ENTRENAMIENTO DE MODELOS"]
        D --> E[Modelo Regresión Lineal OLS]
        D --> F[Modelo Regresión Bayesiana]
        E --> E1[statsmodels.OLS.fit]
        F --> F1[Aproximación Bayesiana]
        E1 --> E2[Guardar modelo_regresion_lineal.pkl]
        F1 --> F2[Guardar modelo_regresion_bayesiana.pkl]
    end
    
    subgraph Fase3["FASE 3: ARQUITECTURA MVC"]
        E2 --> G[ModelService]
        F2 --> G
        G --> H[PredictionController]
        G --> I[StatsController]
        H --> J[API Routes]
        I --> J
        J --> K[Flask App Factory]
        K --> L[Blueprints]
    end
    
    subgraph Fase4["FASE 4: INTERFAZ WEB"]
        L --> M[Rutas Web]
        L --> N[Endpoints API REST]
        M --> O[Templates HTML]
        N --> P[JavaScript Frontend]
        O --> Q[Aplicación Web]
        P --> Q
    end
    
    subgraph Fase5["FASE 5: PREDICCION"]
        Q --> R[Usuario ingresa datos]
        R --> S[POST /api/predecir]
        S --> T[PredictionController]
        T --> U[ModelService]
        U --> V[Modelo OLS]
        U --> W[Modelo Bayesiano]
        V --> X[Predicción OLS]
        W --> Y[Predicción Bayesiana]
        X --> Z[Combinar Resultados]
        Y --> Z
        Z --> AA[Intervalos de Confianza]
        AA --> AB[Respuesta JSON]
        AB --> AC[Visualización en UI]
    end
    
    style Fase1 fill:#e3f2fd
    style Fase2 fill:#f3e5f5
    style Fase3 fill:#e8f5e9
    style Fase4 fill:#fff3e0
    style Fase5 fill:#fce4ec
    style A fill:#bbdefb
    style E2 fill:#c8e6c9
    style F2 fill:#c8e6c9
    style Q fill:#ffccbc
    style AC fill:#c5e1a5
```

## Descripción del Desarrollo

### Fase 1: Preparación de Datos
Se carga el dataset SaratogaHouses.csv, se realiza análisis exploratorio y preprocesamiento de datos, incluyendo la creación de variables dummy para características categóricas.

### Fase 2: Entrenamiento de Modelos
Se entrenan dos modelos estadísticos complementarios:
- **Modelo OLS**: Regresión lineal múltiple usando mínimos cuadrados ordinarios
- **Modelo Bayesiano**: Regresión con inferencia bayesiana usando el Teorema de Bayes

Ambos modelos se guardan como archivos .pkl para su posterior uso.

### Fase 3: Arquitectura MVC
Se implementa una arquitectura Model-View-Controller limpia:
- **Services**: ModelService y StatsService encapsulan la lógica de dominio
- **Controllers**: PredictionController y StatsController orquestan la lógica de negocio
- **Routes**: Blueprints organizan los endpoints de la API y rutas web
- **Factory Pattern**: Flask App Factory permite configuración flexible

### Fase 4: Interfaz Web
Se desarrolla la interfaz de usuario con:
- Templates HTML para la presentación
- JavaScript para la interacción del cliente
- Endpoints API REST para la comunicación backend-frontend
- Bootstrap para el diseño responsive

### Fase 5: Predicción
Flujo completo de predicción:
1. Usuario ingresa datos de la casa
2. Frontend envía petición POST a la API
3. Backend procesa con ambos modelos en paralelo
4. Se combinan resultados y se calculan intervalos de confianza
5. Se retorna respuesta JSON con predicciones
6. Frontend visualiza resultados al usuario

## Tecnologías Utilizadas

- **Backend**: Flask 3.0, Python 3.10
- **Modelos Estadísticos**: statsmodels, scipy
- **Análisis de Datos**: pandas, numpy
- **Frontend**: HTML5, JavaScript, Bootstrap 5
- **Arquitectura**: MVC, Factory Pattern, Blueprints
