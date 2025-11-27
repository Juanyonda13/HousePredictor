"""
Modelo de Regresión Lineal Múltiple para Predicción de Precios de Viviendas
============================================================================

Este módulo implementa un modelo de ESTADÍSTICA CLÁSICA (no Machine Learning)
usando Ordinary Least Squares (OLS) para predicción de precios.

A diferencia de las redes neuronales, este modelo proporciona:
- Coeficientes interpretables con intervalos de confianza
- Pruebas de significancia estadística
- Inferencia estadística formal
- Intervalos de predicción
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import pickle
import os
from typing import Dict, Tuple, List

class ModeloRegresionLineal:
    """Modelo de Regresión Lineal Múltiple para predicción de precios"""
    
    def __init__(self):
        """Inicializa el modelo"""
        self.modelo = None
        self.variables = None
        self.trained = False
        
    def preparar_datos(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepara los datos para el modelo
        
        Args:
            df: DataFrame con los datos de viviendas
            
        Returns:
            Tuple con (X, y) preparados
        """
        # Variables numéricas
        vars_numericas = [
            'metros_habitables', 'metros_totales', 'antiguedad', 'precio_terreno',
            'dormitorios', 'banyos', 'habitaciones', 'chimenea', 'universitarios'
        ]
        
        # Crear variables dummy
        df_prep = df.copy()
        df_prep['tiene_lago'] = (df_prep['vistas_lago'] == 'Yes').astype(int)
        df_prep['tiene_aire'] = (df_prep['aire_acondicionado'] == 'Yes').astype(int)
        df_prep['es_nueva'] = (df_prep['nueva_construccion'] == 'Yes').astype(int)
        
        # Variables finales
        self.variables = vars_numericas + ['tiene_lago', 'tiene_aire', 'es_nueva']
        
        # Preparar X e y
        X = df_prep[self.variables]
        y = df_prep['precio']
        
        # Agregar constante (intercepto)
        X = sm.add_constant(X)
        
        return X, y
    
    def entrenar(self, df: pd.DataFrame) -> Dict:
        """
        Entrena el modelo de regresión lineal
        
        Args:
            df: DataFrame con los datos de entrenamiento
            
        Returns:
            Dict con métricas del modelo
        """
        print("\n Entrenando Modelo de Regresión Lineal Múltiple...")
        
        X, y = self.preparar_datos(df)
        
        # Ajustar modelo OLS
        self.modelo = sm.OLS(y, X).fit()
        self.trained = True
        
        # Calcular métricas
        metricas = {
            'r2': self.modelo.rsquared,
            'r2_ajustado': self.modelo.rsquared_adj,
            'rmse': np.sqrt(self.modelo.mse_resid),
            'aic': self.modelo.aic,
            'bic': self.modelo.bic,
            'n_observaciones': int(self.modelo.nobs)
        }
        
        print(f"\n Modelo entrenado exitosamente")
        print(f"   R²: {metricas['r2']:.4f} ({metricas['r2']*100:.2f}%)")
        print(f"   R² Ajustado: {metricas['r2_ajustado']:.4f}")
        print(f"   RMSE: ${metricas['rmse']:,.2f}")
        print(f"   N observaciones: {metricas['n_observaciones']}")
        
        return metricas
    
    def predecir(self, datos: Dict, incluir_paso_a_paso: bool = False) -> Dict:
        """
        Realiza una predicción con intervalo de confianza
        
        Args:
            datos: Dict con las características de la vivienda
            incluir_paso_a_paso: Si True, incluye el cálculo paso a paso con fórmulas
            
        Returns:
            Dict con predicción e intervalo de confianza
        """
        if not self.trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Preparar datos de entrada
        df_pred = pd.DataFrame([datos])
        
        # Crear variables dummy desde las columnas del DataFrame
        tiene_lago = 0
        tiene_aire = 0
        es_nueva = 0
        
        if 'vistas_lago' in df_pred.columns:
            df_pred['tiene_lago'] = (df_pred['vistas_lago'] == 'Yes').astype(int)
            tiene_lago = int(df_pred['tiene_lago'].iloc[0])
        else:
            df_pred['tiene_lago'] = 0
            
        if 'aire_acondicionado' in df_pred.columns:
            df_pred['tiene_aire'] = (df_pred['aire_acondicionado'] == 'Yes').astype(int)
            tiene_aire = int(df_pred['tiene_aire'].iloc[0])
        else:
            df_pred['tiene_aire'] = 0
            
        if 'nueva_construccion' in df_pred.columns:
            df_pred['es_nueva'] = (df_pred['nueva_construccion'] == 'Yes').astype(int)
            es_nueva = int(df_pred['es_nueva'].iloc[0])
        else:
            df_pred['es_nueva'] = 0
        
        # Seleccionar variables en el orden correcto
        X_pred = df_pred[self.variables]
        
        # Agregar constante (importante: debe llamarse 'const')
        X_pred = sm.add_constant(X_pred, has_constant='add')
        
        # Predicción puntual
        prediccion = self.modelo.predict(X_pred)[0]
        
        # Intervalo de confianza del 95%
        pred_summary = self.modelo.get_prediction(X_pred)
        pred_ci = pred_summary.conf_int(alpha=0.05)
        
        # Obtener coeficientes
        coeficientes = self.modelo.params
        
        resultado = {
            'precio_estimado': float(prediccion),
            'ic_inferior_95': float(pred_ci[0, 0]),
            'ic_superior_95': float(pred_ci[0, 1]),
            'modelo': 'Regresión Lineal Múltiple (OLS)',
            'r2': float(self.modelo.rsquared)
        }
        
        # Agregar paso a paso si se solicita
        if incluir_paso_a_paso:
            resultado['paso_a_paso'] = self._generar_paso_a_paso(
                datos, X_pred.iloc[0], coeficientes, prediccion, pred_ci[0]
            )
        
        return resultado
    
    def _generar_paso_a_paso(self, datos_originales: Dict, X_pred_series: pd.Series, 
                            coeficientes: pd.Series, prediccion: float, 
                            intervalo_confianza: np.ndarray) -> List[Dict]:
        """
        Genera el paso a paso del cálculo con todas las fórmulas estadísticas
        
        Returns:
            Lista de pasos con fórmulas y cálculos
        """
        pasos = []
        
        # Paso 1: Fórmula general
        pasos.append({
            'titulo': 'Fórmula de Regresión Lineal Múltiple (OLS)',
            'descripcion': 'El modelo usa el método de Mínimos Cuadrados Ordinarios (OLS)',
            'formula': 'Precio = β₀ + β₁·X₁ + β₂·X₂ + ... + βₖ·Xₖ + ε',
            'interpretacion': 'Donde β₀ es el intercepto, βᵢ son los coeficientes de cada variable, y ε es el error'
        })
        
        # Paso 2: Preparación de variables
        # Definir tipos de variables aleatorias
        tipos_variables = {
            # Variables numéricas continuas (Normal)
            'metros_habitables': 'Variable Aleatoria Continua (Normal)',
            'metros_totales': 'Variable Aleatoria Continua (Normal)',
            'antiguedad': 'Variable Aleatoria Continua (Normal)',
            'precio_terreno': 'Variable Aleatoria Continua (Normal)',
            'dormitorios': 'Variable Aleatoria Discreta (Entera)',
            'banyos': 'Variable Aleatoria Continua (Normal)',
            'habitaciones': 'Variable Aleatoria Discreta (Entera)',
            'chimenea': 'Variable Aleatoria Discreta (Poisson)',
            'universitarios': 'Variable Aleatoria Continua (Normal)',
            # Variables binarias (Bernoulli/Binomial)
            'tiene_lago': 'Variable Aleatoria Discreta (Bernoulli)',
            'tiene_aire': 'Variable Aleatoria Discreta (Bernoulli)',
            'es_nueva': 'Variable Aleatoria Discreta (Bernoulli)'
        }
        
        variables_preparadas = {}
        tipos_variables_info = {}
        for var in self.variables:
            if var in X_pred_series.index:
                variables_preparadas[var] = float(X_pred_series[var])
                tipos_variables_info[var] = tipos_variables.get(var, 'Variable Aleatoria')
        
        pasos.append({
            'titulo': 'Paso 1: Preparación de Variables',
            'descripcion': 'Se preparan las variables de entrada y se crean variables dummy',
            'variables': variables_preparadas,
            'tipos_variables': tipos_variables_info,
            'formula': 'Variables dummy: tiene_lago = (vistas_lago == "Yes") ? 1 : 0'
        })
        
        # Paso 3: Coeficientes del modelo
        coefs_info = self.obtener_coeficientes()
        
        # Preparar información de coeficientes
        coefs_dict = {}
        for var in coeficientes.index:
            coef_val = float(coeficientes[var])
            if var in coefs_info.index:
                p_val = float(coefs_info.loc[var, 'p_valor'])
                sig = bool(coefs_info.loc[var, 'significativo'])
            else:
                p_val = None
                sig = False
            
            coefs_dict[var] = {
                'valor': coef_val,
                'p_valor': p_val,
                'significativo': sig
            }
        
        pasos.append({
            'titulo': 'Paso 2: Coeficientes del Modelo (β)',
            'descripcion': 'Estos coeficientes fueron estimados mediante OLS (Mínimos Cuadrados Ordinarios) en el entrenamiento. Los coeficientes significativos (p < 0.05) tienen evidencia estadística sólida.',
            'coeficientes': coefs_dict,
            'formula': 'β = (X\'X)⁻¹X\'y (Estimación OLS)'
        })
        
        # Paso 4: Cálculo de la predicción
        calculo_terminos = []
        valor_constante = float(coeficientes.get('const', 0))
        
        for var in self.variables:
            if var in coeficientes.index and var in X_pred_series.index:
                coef = float(coeficientes[var])
                valor = float(X_pred_series[var])
                termino = coef * valor
                calculo_terminos.append({
                    'variable': var,
                    'coeficiente': coef,
                    'valor': valor,
                    'termino': termino,
                    'formula': f'{coef:.2f} × {valor} = {termino:.2f}'
                })
        
        pasos.append({
            'titulo': 'Paso 3: Cálculo de Cada Término',
            'descripcion': 'Se multiplica cada coeficiente por su valor correspondiente',
            'terminos': calculo_terminos,
            'formula': 'Términoᵢ = βᵢ × Xᵢ'
        })
        
        # Paso 5: Suma total
        suma_terminos = sum(term['termino'] for term in calculo_terminos)
        precio_calculado = valor_constante + suma_terminos
        
        pasos.append({
            'titulo': 'Paso 4: Suma Total (Predicción)',
            'descripcion': 'Se suman todos los términos más el intercepto',
            'constante': valor_constante,
            'suma_terminos': suma_terminos,
            'precio_final': precio_calculado,
            'formula': f'Precio = {valor_constante:.2f} + {suma_terminos:.2f} = ${precio_calculado:,.2f}',
            'formula_general': 'Precio = β₀ + Σ(βᵢ × Xᵢ)'
        })
        
        # Paso 6: Intervalo de confianza
        ic_inf = float(intervalo_confianza[0])
        ic_sup = float(intervalo_confianza[1])
        margen_error = (ic_sup - ic_inf) / 2
        
        pasos.append({
            'titulo': 'Paso 5: Intervalo de Confianza al 95%',
            'descripcion': 'Se calcula el intervalo donde el precio real probablemente estará',
            'precio_estimado': precio_calculado,
            'margen_error': margen_error,
            'ic_inferior': ic_inf,
            'ic_superior': ic_sup,
            'formula': f'IC 95% = [${ic_inf:,.2f}, ${ic_sup:,.2f}]',
            'formula_general': 'IC(1-α) = ŷ ± t(α/2, n-k-1) × SE(ŷ)',
            'interpretacion': f'Con 95% de confianza, el precio real está entre ${ic_inf:,.2f} y ${ic_sup:,.2f}'
        })
        
        # Paso 7: Métricas del modelo
        pasos.append({
            'titulo': 'Paso 6: Métricas del Modelo',
            'descripcion': 'Indicadores de calidad del modelo',
            'r2': float(self.modelo.rsquared),
            'r2_ajustado': float(self.modelo.rsquared_adj),
            'rmse': float(np.sqrt(self.modelo.mse_resid)),
            'formula_r2': 'R² = 1 - (SS_res / SS_tot)',
            'interpretacion': f'El modelo explica el {self.modelo.rsquared*100:.2f}% de la varianza en los precios'
        })
        
        return pasos
    
    def obtener_coeficientes(self) -> pd.DataFrame:
        """
        Obtiene los coeficientes del modelo con estadísticas
        
        Returns:
            DataFrame con coeficientes, p-values e IC
        """
        if not self.trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        coef = pd.DataFrame({
            'coeficiente': self.modelo.params,
            'error_std': self.modelo.bse,
            'estadistico_t': self.modelo.tvalues,
            'p_valor': self.modelo.pvalues,
            'ic_inferior': self.modelo.conf_int()[0],
            'ic_superior': self.modelo.conf_int()[1]
        })
        
        coef['significativo'] = coef['p_valor'] < 0.05
        
        return coef
    
    def guardar(self, ruta: str = 'model/modelo_regresion_lineal.pkl'):
        """Guarda el modelo entrenado"""
        if not self.trained:
            raise ValueError("No hay modelo entrenado para guardar")
        
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        with open(ruta, 'wb') as f:
            pickle.dump({
                'modelo': self.modelo,
                'variables': self.variables
            }, f)
        
        print(f" Modelo guardado en: {ruta}")
    
    @classmethod
    def cargar(cls, ruta: str = 'model/modelo_regresion_lineal.pkl'):
        """Carga un modelo previamente guardado"""
        instancia = cls()
        
        with open(ruta, 'rb') as f:
            data = pickle.load(f)
        
        # Compatibilidad: manejar tanto dict como modelo directo
        if isinstance(data, dict):
            instancia.modelo = data['modelo']
            instancia.variables = data['variables']
        else:
            # Si es el modelo directo (guardado por analisis_estadistico.py)
            instancia.modelo = data
            # Cargar variables desde archivo separado
            vars_file = 'model/variables_modelo.pkl'
            if os.path.exists(vars_file):
                with open(vars_file, 'rb') as vf:
                    instancia.variables = pickle.load(vf)
            else:
                # Variables por defecto
                instancia.variables = [
                    'metros_habitables', 'metros_totales', 'antiguedad', 'precio_terreno',
                    'dormitorios', 'banyos', 'habitaciones', 'chimenea', 'universitarios',
                    'tiene_lago', 'tiene_aire', 'es_nueva'
                ]
        
        instancia.trained = True
        
        print(f" Modelo cargado desde: {ruta}")
        return instancia


def entrenar_y_guardar():
    """
    Función principal para entrenar y guardar el modelo
    """
    print("="*80)
    print(" ENTRENAMIENTO DE MODELO DE REGRESIÓN LINEAL MÚLTIPLE")
    print("="*80)
    
    # Cargar datos
    print("\n📥 Cargando datos...")
    df = pd.read_csv('data/SaratogaHouses.csv')
    print(f" {len(df)} observaciones cargadas")
    
    # Crear y entrenar modelo
    modelo = ModeloRegresionLineal()
    metricas = modelo.entrenar(df)
    
    # Mostrar coeficientes significativos
    print("\n Coeficientes Estadísticamente Significativos (p < 0.05):")
    coefs = modelo.obtener_coeficientes()
    coefs_sig = coefs[coefs['significativo']].drop('const', errors='ignore')
    
    for idx, row in coefs_sig.iterrows():
        print(f"   {idx:25s}: β = {row['coeficiente']:>10.2f}, p = {row['p_valor']:.4f}")
    
    # Guardar modelo
    modelo.guardar()
    
    # Guardar también variables
    with open('model/variables_modelo.pkl', 'wb') as f:
        pickle.dump(modelo.variables, f)
    
    print("\n" + "="*80)
    print(" ENTRENAMIENTO COMPLETADO")
    print("="*80)
    
    return modelo


if __name__ == '__main__':
    # Entrenar y guardar modelo si se ejecuta directamente
    modelo = entrenar_y_guardar()
    
    # Ejemplo de predicción
    print("\nPRUEBA DE PREDICCION:")
    ejemplo = {
        'metros_totales': 0.49,
        'antiguedad': 15,
        'precio_terreno': 25000,
        'metros_habitables': 1592,
        'universitarios': 54,
        'dormitorios': 3,
        'chimenea': 1,
        'banyos': 1.5,
        'habitaciones': 8,
        'vistas_lago': 'No',
        'nueva_construccion': 'No',
        'aire_acondicionado': 'No'
    }
    
    resultado = modelo.predecir(ejemplo)
    print(f"\n Precio estimado: ${resultado['precio_estimado']:,.2f}")
    print(f" Intervalo de confianza 95%:")
    print(f"   [${resultado['ic_inferior_95']:,.2f}, ${resultado['ic_superior_95']:,.2f}]")
    print(f"\n Modelo: {resultado['modelo']}")
    print(f" R²: {resultado['r2']:.4f} ({resultado['r2']*100:.2f}%)")

