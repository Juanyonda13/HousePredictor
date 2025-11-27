"""
Módulo para hacer predicciones con el modelo entrenado
"""

import pandas as pd
import joblib
import os


class PredictorCasas:
    """Clase para manejar predicciones de precios de casas"""
    
    def __init__(self):
        """Inicializa el predictor cargando el modelo entrenado"""
        model_path = 'model/modelo_casas.pkl'
        preprocessor_path = 'model/preprocessor.pkl'
        columns_path = 'model/columns.pkl'
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "Modelo no encontrado. Ejecuta 'python model/train.py' primero."
            )
        
        self.modelo = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        self.columns_info = joblib.load(columns_path)
        
    def predecir(self, datos_casa):
        """
        Predice el precio de una casa
        
        Args:
            datos_casa (dict): Diccionario con las características de la casa
            
        Returns:
            float: Precio predicho
        """
        # Convertir a DataFrame
        casa_df = pd.DataFrame([datos_casa])
        
        # Preprocesar
        casa_prep = self.preprocessor.transform(casa_df)
        
        # Predecir
        precio = self.modelo.predict(casa_prep)[0]
        
        return precio
    
    def predecir_batch(self, lista_casas):
        """
        Predice precios para múltiples casas
        
        Args:
            lista_casas (list): Lista de diccionarios con características
            
        Returns:
            list: Lista de precios predichos
        """
        if not lista_casas:
            return []
        
        # Convertir a DataFrame
        casas_df = pd.DataFrame(lista_casas)
        
        # Preprocesar
        casas_prep = self.preprocessor.transform(casas_df)
        
        # Predecir
        precios = self.modelo.predict(casas_prep)
        
        return precios.tolist()
    
    def obtener_parametros(self):
        """Retorna los parámetros del modelo"""
        return self.modelo.get_params()
    
    @staticmethod
    def crear_datos_ejemplo():
        """Crea datos de ejemplo para testing"""
        return {
            'metros_totales': 0.49,
            'antiguedad': 15,
            'precio_terreno': 25000,
            'metros_habitables': 1592,
            'universitarios': 54,
            'dormitorios': 3,
            'chimenea': 1,
            'banyos': 1.5,
            'habitaciones': 8,
            'calefaccion': 'hot air',
            'consumo_calefacion': 'gas',
            'desague': 'septic',
            'vistas_lago': 'No',
            'nueva_construccion': 'No',
            'aire_acondicionado': 'No'
        }
    
    @staticmethod
    def validar_entrada(datos):
        """
        Valida que los datos de entrada tengan el formato correcto
        
        Args:
            datos (dict): Datos a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        campos_requeridos = [
            'metros_totales', 'antiguedad', 'precio_terreno',
            'metros_habitables', 'universitarios', 'dormitorios',
            'chimenea', 'banyos', 'habitaciones', 'calefaccion',
            'consumo_calefacion', 'desague', 'vistas_lago',
            'nueva_construccion', 'aire_acondicionado'
        ]
        
        # Verificar campos requeridos
        for campo in campos_requeridos:
            if campo not in datos:
                return False, f"Campo faltante: {campo}"
        
        # Validar tipos numéricos
        campos_numericos = [
            'metros_totales', 'antiguedad', 'precio_terreno',
            'metros_habitables', 'universitarios', 'dormitorios',
            'chimenea', 'banyos', 'habitaciones'
        ]
        
        for campo in campos_numericos:
            try:
                float(datos[campo])
            except (ValueError, TypeError):
                return False, f"Campo '{campo}' debe ser numérico"
        
        return True, "OK"


# Función helper para usar desde Flask
def predecir_precio_casa(datos_casa):
    """
    Función helper para predecir desde Flask
    
    Args:
        datos_casa (dict): Características de la casa
        
    Returns:
        dict: Resultado con precio o error
    """
    try:
        predictor = PredictorCasas()
        
        # Validar entrada
        es_valido, mensaje = PredictorCasas.validar_entrada(datos_casa)
        if not es_valido:
            return {'error': mensaje, 'precio': None}
        
        # Predecir
        precio = predictor.predecir(datos_casa)
        
        return {
            'precio': float(precio),
            'precio_formateado': f"${precio:,.2f}",
            'error': None
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'precio': None
        }

