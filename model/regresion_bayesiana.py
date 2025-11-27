"""
Modelo de Regresión Bayesiana para Predicción de Precios de Viviendas
============================================================================

Este módulo implementa un modelo de ESTADÍSTICA BAYESIANA usando el
Teorema de Bayes para estimar coeficientes con distribuciones de probabilidad.

A diferencia de OLS (frecuentista), este modelo:
- Usa distribuciones previas (priors) para los coeficientes
- Actualiza con los datos usando el Teorema de Bayes
- Proporciona distribuciones posteriores (posteriors) para los coeficientes
- Calcula intervalos creíbles (credible intervals) en lugar de intervalos de confianza
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.weightstats import DescrStatsW
import pickle
import os
from typing import Dict, Tuple, List
from scipy import stats


class ModeloRegresionBayesiana:
    """Modelo de Regresión Bayesiana para predicción de precios"""
    
    def __init__(self):
        """Inicializa el modelo"""
        self.modelo = None
        self.variables = None
        self.trained = False
        self.priors = {}  # Distribuciones previas
        self.posteriors = {}  # Distribuciones posteriores
        
    def preparar_datos(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepara los datos para el modelo (igual que OLS)
        
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
        Entrena el modelo de regresión bayesiana
        
        Usa aproximación por MCMC (Markov Chain Monte Carlo) o 
        aproximación normal para distribución posterior
        
        Args:
            df: DataFrame con los datos de entrenamiento
            
        Returns:
            Dict con métricas del modelo
        """
        print("\n Entrenando Modelo de Regresión Bayesiana...")
        
        X, y = self.preparar_datos(df)
        
        # Para este ejemplo, usamos aproximación bayesiana con statsmodels
        # que estima la distribución posterior de los coeficientes
        
        # Primero ajustamos modelo OLS para obtener valores iniciales
        modelo_ols = sm.OLS(y, X).fit()
        
        # Usamos Bayesian Information Criterion (BIC) para comparar modelos
        # y aproximamos la distribución posterior usando distribución normal
        
        # Para una aproximación bayesiana más simple, usamos:
        # - Prior no informativo (flat prior) → distribución posterior ≈ OLS
        # - Prior informativo → actualización bayesiana
        
        # Aproximación: Usar OLS como base y calcular distribución posterior
        # con varianza estimada
        
        # Estimación de la varianza del error
        residuos = modelo_ols.resid
        n = len(y)
        k = X.shape[1]  # número de parámetros
        
        # Varianza residual
        sigma2 = np.var(residuos, ddof=k)
        
        # Coeficientes (media posterior)
        beta_media = modelo_ols.params
        
        # Matriz de covarianza posterior (aproximación)
        # Para prior no informativo, la distribución posterior es:
        # β ~ Normal(β_ols, (X'X)^(-1) * σ²)
        XX_inv = np.linalg.inv(X.T @ X)
        beta_cov = XX_inv * sigma2
        
        # Convertir a DataFrame para facilitar acceso
        beta_cov_df = pd.DataFrame(beta_cov, index=beta_media.index, columns=beta_media.index)
        
        # Guardar distribuciones posteriores
        self.modelo = modelo_ols  # Guardamos OLS como base
        self.beta_media = beta_media
        self.beta_cov = beta_cov_df  # DataFrame para facilitar acceso
        self.beta_cov_matrix = beta_cov  # Matriz numpy para cálculos
        self.sigma2 = sigma2
        self.X_train = X
        self.y_train = y
        
        # Priors (no informativos para este caso)
        # P(β) ~ Normal(0, ∞) → prior no informativo
        self.priors = {
            'tipo': 'No informativo (flat prior)',
            'distribucion': 'Normal con varianza infinita'
        }
        
        # Posteriors
        self.posteriors = {
            'distribucion': 'Normal Multivariada',
            'media': beta_media,
            'covarianza': beta_cov
        }
        
        self.trained = True
        
        # Calcular métricas (R² es el mismo que OLS en aproximación)
        metricas = {
            'r2': modelo_ols.rsquared,
            'r2_ajustado': modelo_ols.rsquared_adj,
            'rmse': np.sqrt(modelo_ols.mse_resid),
            'bic': modelo_ols.bic,
            'aic': modelo_ols.aic,
            'n_observaciones': int(n)
        }
        
        print(f"\n Modelo Bayesiano entrenado exitosamente")
        print(f"   Prior: {self.priors['tipo']}")
        print(f"   Posterior: {self.posteriors['distribucion']}")
        print(f"   R²: {metricas['r2']:.4f} ({metricas['r2']*100:.2f}%)")
        print(f"   RMSE: ${metricas['rmse']:,.2f}")
        print(f"   N observaciones: {metricas['n_observaciones']}")
        
        return metricas
    
    def predecir(self, datos: Dict, incluir_paso_a_paso: bool = False) -> Dict:
        """
        Realiza una predicción usando regresión bayesiana con intervalo creíble
        
        Args:
            datos: Dict con las características de la vivienda
            incluir_paso_a_paso: Si True, incluye el cálculo paso a paso con fórmulas
            
        Returns:
            Dict con predicción e intervalo creíble
        """
        if not self.trained:
            raise ValueError("El modelo no ha sido entrenado")
        
        # Preparar datos de entrada
        df_pred = pd.DataFrame([datos])
        
        # Crear variables dummy
        if 'vistas_lago' in df_pred.columns:
            df_pred['tiene_lago'] = (df_pred['vistas_lago'] == 'Yes').astype(int)
        else:
            df_pred['tiene_lago'] = 0
            
        if 'aire_acondicionado' in df_pred.columns:
            df_pred['tiene_aire'] = (df_pred['aire_acondicionado'] == 'Yes').astype(int)
        else:
            df_pred['tiene_aire'] = 0
            
        if 'nueva_construccion' in df_pred.columns:
            df_pred['es_nueva'] = (df_pred['nueva_construccion'] == 'Yes').astype(int)
        else:
            df_pred['es_nueva'] = 0
        
        # Seleccionar variables en el orden correcto
        X_pred = df_pred[self.variables]
        
        # Agregar constante
        X_pred = sm.add_constant(X_pred, has_constant='add')
        
        # Predicción puntual (media posterior)
        prediccion_puntual = (X_pred.iloc[0] @ self.beta_media)
        
        # Varianza de la predicción (distribución predictiva posterior)
        # Var(ŷ) = X' * Var(β) * X + σ²
        x_vec = X_pred.iloc[0].values.reshape(-1, 1)
        var_prediccion = float(x_vec.T @ self.beta_cov_matrix @ x_vec) + self.sigma2
        std_prediccion = np.sqrt(var_prediccion)
        
        # Intervalo creíble al 95% (usando distribución t de Student)
        # Para n grande, aproximamos con normal
        from scipy.stats import t
        # Usar nobs del modelo OLS (que siempre está disponible) en lugar de y_train
        n_observaciones = self.modelo.nobs if hasattr(self.modelo, 'nobs') else (len(self.y_train) if hasattr(self, 'y_train') and self.y_train is not None else 1000)
        df_residual = n_observaciones - len(self.variables) - 1
        t_critico = t.ppf(0.975, df_residual)
        
        # Intervalo creíble bayesiano
        ic_inferior = prediccion_puntual - t_critico * std_prediccion
        ic_superior = prediccion_puntual + t_critico * std_prediccion
        
        # Obtener coeficientes para paso a paso
        coeficientes = self.beta_media
        
        resultado = {
            'precio_estimado': float(prediccion_puntual),
            'ic_inferior_95': float(ic_inferior),
            'ic_superior_95': float(ic_superior),
            'modelo': 'Regresión Bayesiana (Teorema de Bayes)',
            'r2': float(self.modelo.rsquared),
            'desviacion_estandar': float(std_prediccion),
            'tipo_intervalo': 'Intervalo Creíble (Bayesiano)'
        }
        
        # Agregar paso a paso si se solicita
        if incluir_paso_a_paso:
            resultado['paso_a_paso'] = self._generar_paso_a_paso_bayesiano(
                datos, X_pred.iloc[0], coeficientes, prediccion_puntual, 
                ic_inferior, ic_superior, std_prediccion
            )
        
        return resultado
    
    def _generar_paso_a_paso_bayesiano(self, datos_originales: Dict, 
                                      X_pred_series: pd.Series,
                                      coeficientes: pd.Series,
                                      prediccion: float,
                                      ic_inferior: float,
                                      ic_superior: float,
                                      std_prediccion: float) -> List[Dict]:
        """
        Genera el paso a paso del cálculo bayesiano con todas las fórmulas
        
        Returns:
            Lista de pasos con fórmulas bayesianas
        """
        pasos = []
        
        # Paso 1: Teorema de Bayes aplicado a regresión
        pasos.append({
            'titulo': 'Teorema de Bayes Aplicado a Regresión',
            'descripcion': 'El modelo usa el Teorema de Bayes para actualizar nuestras creencias sobre los coeficientes β',
            'formula': 'P(β|datos) = [P(datos|β) × P(β)] / P(datos)',
            'formula_desarrollada': 'P(β|datos) ∝ P(datos|β) × P(β)',
            'interpretacion': 'La probabilidad posterior P(β|datos) se actualiza combinando la verosimilitud P(datos|β) con la probabilidad previa P(β)',
            'formula_nombres': 'Posterior ∝ Verosimilitud × Prior'
        })
        
        # Paso 2: Prior (Distribución previa)
        pasos.append({
            'titulo': 'Paso 1: Distribución Previo (Prior) P(β)',
            'descripcion': 'Antes de ver los datos, asumimos una distribución previa para los coeficientes. En este caso, usamos un prior no informativo.',
            'prior_tipo': self.priors['tipo'],
            'prior_formula': 'P(β) ~ Normal(0, ∞) (Prior no informativo)',
            'formula': 'P(β) = constante (prior uniforme/no informativo)',
            'interpretacion': 'Un prior no informativo significa que no tenemos conocimiento previo sobre los coeficientes, permitiendo que los datos hablen'
        })
        
        # Paso 3: Verosimilitud
        pasos.append({
            'titulo': 'Paso 2: Verosimilitud P(datos|β)',
            'descripcion': 'La verosimilitud mide qué tan probables son los datos observados dados los coeficientes β',
            'formula': 'P(datos|β) = ∏ P(yᵢ|xᵢ, β)',
            'formula_desarrollada': 'L(β) = ∏ (1/√(2πσ²)) × exp(-(yᵢ - xᵢβ)²/(2σ²))',
            'interpretacion': 'Maximizar la verosimilitud es equivalente a minimizar los errores cuadráticos (como en OLS)',
            'formula_estimacion': 'β_ML = argmax L(β) = (X\'X)⁻¹X\'y'
        })
        
        # Paso 4: Posterior (Distribución posterior)
        pasos.append({
            'titulo': 'Paso 3: Distribución Posterior P(β|datos)',
            'descripcion': 'Después de ver los datos, actualizamos nuestras creencias usando el Teorema de Bayes',
            'posterior_tipo': self.posteriors['distribucion'],
            'formula': 'P(β|datos) ~ Normal(β_media, Σ_β)',
            'formula_desarrollada': 'β|datos ~ Normal((X\'X)⁻¹X\'y, (X\'X)⁻¹σ²)',
            'beta_media': dict(self.beta_media),
            'interpretacion': 'La distribución posterior combina el prior con la información de los datos observados'
        })
        
        # Paso 5: Preparación de variables (igual que OLS)
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
            'titulo': 'Paso 4: Preparación de Variables',
            'descripcion': 'Se preparan las variables de entrada para la predicción',
            'variables': variables_preparadas,
            'tipos_variables': tipos_variables_info,
            'formula': 'Variables dummy: tiene_lago = (vistas_lago == "Yes") ? 1 : 0'
        })
        
        # Paso 6: Coeficientes posteriores
        coefs_dict = {}
        for var in coeficientes.index:
            coef_val = float(coeficientes[var])
            # Varianza del coeficiente (diagonal de la matriz de covarianza)
            var_coef = float(self.beta_cov.loc[var, var] if hasattr(self.beta_cov, 'loc') else self.beta_cov.iloc[coeficientes.index.get_loc(var), coeficientes.index.get_loc(var)])
            std_coef = np.sqrt(var_coef)
            
            # Obtener varianza de la matriz de covarianza
            try:
                if var in self.beta_cov.index:
                    var_coef = float(self.beta_cov.loc[var, var])
                    std_coef = np.sqrt(var_coef)
                else:
                    std_coef = 0.0
            except:
                std_coef = 0.0
            
            coefs_dict[var] = {
                'valor': coef_val,
                'desviacion_estandar': std_coef,
                'interpretacion': f'Coeficiente con distribución posterior ~ Normal({coef_val:.2f}, {std_coef:.2f}²)'
            }
        
        pasos.append({
            'titulo': 'Paso 5: Coeficientes Posteriores P(β|datos)',
            'descripcion': 'Cada coeficiente tiene una distribución posterior que refleja nuestra incertidumbre después de ver los datos',
            'coeficientes': coefs_dict,
            'formula': 'βᵢ|datos ~ Normal(μᵢ, σᵢ²)',
            'interpretacion': 'Los coeficientes no son valores fijos sino distribuciones de probabilidad'
        })
        
        # Paso 7: Predicción bayesiana
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
            'titulo': 'Paso 6: Cálculo de Predicción Puntual',
            'descripcion': 'Usamos la media de la distribución posterior para hacer la predicción puntual',
            'terminos': calculo_terminos,
            'constante': valor_constante,
            'suma_terminos': sum(term['termino'] for term in calculo_terminos),
            'formula': 'E[y|X] = X × E[β|datos] = X × β_media',
            'formula_desarrollada': f'Precio = {valor_constante:.2f} + Σ(βᵢ × Xᵢ)',
            'interpretacion': 'La predicción usa el valor esperado (media) de la distribución posterior de los coeficientes'
        })
        
        # Paso 8: Distribución predictiva posterior
        suma_terminos = sum(term['termino'] for term in calculo_terminos)
        precio_calculado = valor_constante + suma_terminos
        
        pasos.append({
            'titulo': 'Paso 7: Distribución Predictiva Posterior',
            'descripcion': 'La incertidumbre en la predicción viene de la incertidumbre en los coeficientes y en el error',
            'precio_estimado': precio_calculado,
            'varianza_prediccion': float(std_prediccion ** 2),
            'desviacion_estandar': float(std_prediccion),
            'formula': 'Var(y|X) = X\'Var(β|datos)X + σ²',
            'formula_desarrollada': f'Desviación estándar = {std_prediccion:.2f}',
            'interpretacion': 'La varianza de la predicción combina la incertidumbre de los coeficientes con la incertidumbre del error'
        })
        
        # Paso 9: Intervalo creíble
        margen_error = (ic_superior - ic_inferior) / 2
        
        pasos.append({
            'titulo': 'Paso 8: Intervalo Creíble al 95% (Bayesiano)',
            'descripcion': 'El intervalo creíble bayesiano contiene el 95% de la distribución posterior del precio',
            'precio_estimado': precio_calculado,
            'margen_error': margen_error,
            'ic_inferior': ic_inferior,
            'ic_superior': ic_superior,
            'formula': f'IC 95% = [${ic_inferior:,.2f}, ${ic_superior:,.2f}]',
            'formula_general': 'IC(95%) = E[y|X] ± t₀.₀₂₅ × √Var(y|X)',
            'interpretacion': f'Con 95% de probabilidad (credibilidad bayesiana), el precio está entre ${ic_inferior:,.2f} y ${ic_superior:,.2f}',
            'diferencia_ols': 'A diferencia de los intervalos de confianza (frecuentistas), los intervalos creíbles tienen interpretación probabilística directa'
        })
        
        # Paso 10: Comparación con OLS
        pasos.append({
            'titulo': 'Paso 9: Comparación: Bayesiano vs Frecuentista (OLS)',
            'descripcion': 'Diferencias clave entre los enfoques estadísticos',
            'comparacion': {
                'bayesiano': {
                    'coeficientes': 'Distribuciones de probabilidad P(β|datos)',
                    'interpretacion': 'Coeficientes son variables aleatorias',
                    'intervalos': 'Intervalos creíbles (probabilidad directa)',
                    'formula': 'P(β|datos) ∝ P(datos|β) × P(β)'
                },
                'frecuentista': {
                    'coeficientes': 'Valores fijos estimados',
                    'interpretacion': 'Coeficientes son parámetros desconocidos',
                    'intervalos': 'Intervalos de confianza (repetición de muestreo)',
                    'formula': 'β = (X\'X)⁻¹X\'y'
                }
            },
            'ventaja_bayesiana': 'Permite incorporar conocimiento previo y proporciona interpretación probabilística directa'
        })
        
        return pasos
    
    def guardar(self, ruta: str = 'model/modelo_regresion_bayesiana.pkl'):
        """Guarda el modelo entrenado"""
        if not self.trained:
            raise ValueError("No hay modelo entrenado para guardar")
        
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        with open(ruta, 'wb') as f:
            pickle.dump({
                'modelo': self.modelo,
                'beta_media': self.beta_media,
                'beta_cov': self.beta_cov,
                'sigma2': self.sigma2,
                'variables': self.variables,
                'priors': self.priors,
                'posteriors': self.posteriors
            }, f)
        
        print(f" Modelo Bayesiano guardado en: {ruta}")
    
    @classmethod
    def cargar(cls, ruta: str = 'model/modelo_regresion_bayesiana.pkl'):
        """Carga un modelo previamente guardado"""
        instancia = cls()
        
        with open(ruta, 'rb') as f:
            data = pickle.load(f)
        
        instancia.modelo = data['modelo']
        instancia.beta_media = data['beta_media']
        beta_cov = data['beta_cov']
        # Convertir a DataFrame si es matriz numpy
        if isinstance(beta_cov, np.ndarray):
            instancia.beta_cov = pd.DataFrame(beta_cov, index=instancia.beta_media.index, columns=instancia.beta_media.index)
            instancia.beta_cov_matrix = beta_cov
        else:
            instancia.beta_cov = beta_cov
            instancia.beta_cov_matrix = beta_cov.values if hasattr(beta_cov, 'values') else beta_cov
        instancia.sigma2 = data['sigma2']
        instancia.variables = data['variables']
        instancia.priors = data.get('priors', {})
        instancia.posteriors = data.get('posteriors', {})
        instancia.trained = True
        
        print(f" Modelo Bayesiano cargado desde: {ruta}")
        return instancia


def entrenar_y_guardar_bayesiano():
    """
    Función principal para entrenar y guardar el modelo bayesiano
    """
    print("="*80)
    print(" ENTRENAMIENTO DE MODELO DE REGRESIÓN BAYESIANA")
    print("="*80)
    
    # Cargar datos
    print("\n📥 Cargando datos...")
    df = pd.read_csv('data/SaratogaHouses.csv')
    print(f" {len(df)} observaciones cargadas")
    
    # Crear y entrenar modelo
    modelo = ModeloRegresionBayesiana()
    metricas = modelo.entrenar(df)
    
    # Guardar modelo
    modelo.guardar()
    
    print("\n" + "="*80)
    print(" ENTRENAMIENTO BAYESIANO COMPLETADO")
    print("="*80)
    
    return modelo


if __name__ == '__main__':
    # Entrenar y guardar modelo si se ejecuta directamente
    modelo = entrenar_y_guardar_bayesiano()
    
    # Ejemplo de predicción
    print("\nPRUEBA DE PREDICCIÓN BAYESIANA:")
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
    print(f" Intervalo creíble 95%:")
    print(f"   [${resultado['ic_inferior_95']:,.2f}, ${resultado['ic_superior_95']:,.2f}]")
    print(f"\n Modelo: {resultado['modelo']}")
    print(f" R²: {resultado['r2']:.4f} ({resultado['r2']*100:.2f}%)")

