# 🚀 Inicio Rápido

## Opción 1: Script Automático (Recomendado)

```bash
cd /home/juanyonda/projects/prediccion-casas-ml
./start.sh
```

## Opción 2: Manual

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Entrenar el modelo (solo la primera vez)
```bash
python model/train.py
```

### Paso 3: Iniciar la aplicación
```bash
python app.py
```

### Paso 4: Abrir en el navegador
```
http://127.0.0.1:5000
```

---

## ✨ Funcionalidades

- **Predictor:** http://127.0.0.1:5000/
- **Mapa Interactivo:** http://127.0.0.1:5000/mapa

---

## 📊 API Endpoints

- `POST /api/predecir` - Predecir precio
- `GET /api/estadisticas` - Ver estadísticas
- `GET /api/modelo-info` - Info del modelo
- `GET /api/datos-ejemplo` - Datos de ejemplo

---

## 🆘 Problemas Comunes

**Modelo no encontrado:**
```bash
python model/train.py
```

**Puerto ocupado:**
Cambia el puerto en `app.py` línea final a `port=5001`

---

**Para más detalles, lee [README.md](README.md)**

