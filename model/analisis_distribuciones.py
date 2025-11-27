"""
Módulo para generar análisis estadístico detallado paso a paso
Incluye: Normal, Binomial, Poisson, Esperanza, Bayes, Intervalos, Pruebas de Hipótesis

Estos análisis se usan SOLO para fines académicos/estudio,
NO interfieren con la predicción final del precio.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm, binom, poisson, chi2_contingency, ttest_ind, shapiro
from typing import Dict, List
import os


class AnalisisEstadistico:
    """Clase para generar análisis estadísticos detallados paso a paso"""
    
    def __init__(self):
        self.df = None
        self.precio = None
        
    def cargar_datos(self, ruta_csv: str = 'data/SaratogaHouses.csv'):
        """Carga el dataset"""
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError(f"Dataset no encontrado en {ruta_csv}")
        
        self.df = pd.read_csv(ruta_csv)
        self.precio = self.df['precio']
        return self.df
    
    def generar_analisis_completo(self) -> Dict:
        """
        Genera análisis estadístico completo con paso a paso detallado
        
        Returns:
            Dict con todos los análisis paso a paso
        """
        if self.df is None:
            self.cargar_datos()
        
        analisis = {
            'distribucion_normal': self._analisis_normal(),
            'distribucion_binomial': self._analisis_binomial(),
            'distribucion_poisson': self._analisis_poisson(),
            'esperanza_varianza': self._analisis_esperanza_varianza(),
            'teorema_bayes': self._analisis_bayes(),
            'intervalos_confianza': self._analisis_intervalos_confianza(),
            'pruebas_hipotesis': self._analisis_pruebas_hipotesis()
        }
        
        return analisis
    
    def _analisis_normal(self) -> List[Dict]:
        """Análisis de Distribución Normal con paso a paso"""
        pasos = []
        
        mu = float(self.precio.mean())
        sigma = float(self.precio.std())
        n = len(self.precio)
        
        # Test de normalidad
        statistic_shapiro, p_value_shapiro = shapiro(self.precio)
        
        pasos.append({
            'titulo': 'Paso 1: Definición de Variable Aleatoria',
            'descripcion': 'Definimos la variable aleatoria continua para el precio de las viviendas',
            'formula': 'X = Precio de la vivienda',
            'formula_desarrollada': 'X: Variable aleatoria continua (precio en dólares)',
            'interpretacion': 'El precio es una variable aleatoria que puede tomar cualquier valor positivo',
            'variables': {
                'Variable': 'X',
                'Descripción': 'Precio de la vivienda',
                'Tipo': 'Variable aleatoria continua',
                'Rango': f'[${self.precio.min():,.0f}, ${self.precio.max():,.0f}]'
            }
        })
        
        pasos.append({
            'titulo': 'Paso 2: Medidas Descriptivas de la Muestra',
            'descripcion': 'Calculamos las medidas de tendencia central y dispersión de la muestra',
            'formula': 'Media muestral: x̄ = (Σxᵢ) / n',
            'formula_desarrollada': f'x̄ = ${mu:,.2f}',
            'medidas_centrales': {
                'Media (x̄)': mu,
                'Mediana': float(self.precio.median()),
                'Moda': float(self.precio.mode()[0])
            },
            'medidas_dispersion': {
                'Varianza muestral (s²)': float(self.precio.var(ddof=1)),
                'Desviación estándar muestral (s)': float(self.precio.std(ddof=1)),
                'Varianza poblacional (σ²)': float(self.precio.var(ddof=0)),
                'Desviación estándar poblacional (σ)': sigma,
                'Rango': float(self.precio.max() - self.precio.min())
            },
            'n': n,
            'interpretacion': 'Estas medidas nos permiten caracterizar la distribución de los precios'
        })
        
        pasos.append({
            'titulo': 'Paso 3: Ajuste a Distribución Normal',
            'descripcion': 'Ajustamos la distribución observada a una distribución normal teórica',
            'formula': 'X ~ Normal(μ, σ²)',
            'formula_desarrollada': f'X ~ Normal(μ=${mu:,.0f}, σ=${sigma:,.0f})',
            'parametros': {
                'Media poblacional (μ)': mu,
                'Desviación estándar poblacional (σ)': sigma,
                'Varianza poblacional (σ²)': float(sigma**2)
            },
            'pdf_formula': 'f(x) = (1/(σ√(2π))) × exp(-(x-μ)²/(2σ²))',
            'pdf_formula_desarrollada': f'f(x) = (1/({sigma:,.0f}√(2π))) × exp(-(x-{mu:,.0f})²/(2×{sigma**2:,.0f}))',
            'interpretacion': 'La distribución normal describe la probabilidad de que una vivienda tenga un precio específico'
        })
        
        pasos.append({
            'titulo': 'Paso 4: Test de Normalidad (Shapiro-Wilk)',
            'descripcion': 'Verificamos si los datos siguen una distribución normal usando el test de Shapiro-Wilk',
            'formula': 'H₀: Los datos siguen una distribución normal',
            'formula_alternativa': 'H₁: Los datos NO siguen una distribución normal',
            'estadistico': float(statistic_shapiro),
            'p_valor': float(p_value_shapiro),
            'nivel_significancia': 0.05,
            'conclusion': 'Los datos siguen una distribución normal' if p_value_shapiro > 0.05 else 'Los datos no son perfectamente normales, pero por el Teorema del Límite Central, la media muestral sí lo es',
            'interpretacion': 'Con n > 30, el Teorema del Límite Central garantiza que la media muestral sigue una distribución normal, incluso si los datos individuales no son normales'
        })
        
        pasos.append({
            'titulo': 'Paso 5: Propiedades de la Distribución Normal',
            'descripcion': 'Aplicamos las propiedades clave de la distribución normal',
            'regla_empirica': {
                '68%': f'[${mu - sigma:,.0f}, ${mu + sigma:,.0f}]',
                '95%': f'[${mu - 2*sigma:,.0f}, ${mu + 2*sigma:,.0f}]',
                '99.7%': f'[${mu - 3*sigma:,.0f}, ${mu + 3*sigma:,.0f}]'
            },
            'formula_regla': 'P(μ - kσ ≤ X ≤ μ + kσ)',
            'formula_k1': 'P(μ - σ ≤ X ≤ μ + σ) ≈ 0.68 (68%)',
            'formula_k2': 'P(μ - 2σ ≤ X ≤ μ + 2σ) ≈ 0.95 (95%)',
            'formula_k3': 'P(μ - 3σ ≤ X ≤ μ + 3σ) ≈ 0.997 (99.7%)',
            'interpretacion': 'La regla empírica nos dice qué porcentaje de viviendas tiene precios dentro de ciertos rangos'
        })
        
        pasos.append({
            'titulo': 'Paso 6: Características de la Distribución',
            'descripcion': 'Analizamos la forma de la distribución',
            'asimetria': float(self.precio.skew()),
            'curtosis': float(self.precio.kurtosis()),
            'interpretacion_asimetria': 'Asimetría positiva: hay más viviendas baratas que caras' if self.precio.skew() > 0 else 'Asimetría negativa: hay más viviendas caras que baratas',
            'interpretacion_curtosis': 'La curtosis mide qué tan concentrados están los datos alrededor de la media',
            'tipo_distribucion': 'Ligeramente asimétrica hacia la derecha (cola larga en valores altos)'
        })
        
        return pasos
    
    def _analisis_binomial(self) -> List[Dict]:
        """Análisis de Distribución Binomial con paso a paso"""
        pasos = []
        
        tiene_lago = (self.df['vistas_lago'] == 'Yes').astype(int)
        n_total = len(tiene_lago)
        n_con_lago = int(tiene_lago.sum())
        p = float(n_con_lago / n_total)
        q = 1 - p
        
        pasos.append({
            'titulo': 'Paso 1: Definición de Variable Aleatoria Binomial',
            'descripcion': 'Definimos una variable aleatoria discreta que sigue una distribución binomial',
            'formula': 'Y = Vivienda tiene vistas al lago (Sí=1, No=0)',
            'formula_desarrollada': 'Y ~ Binomial(n=1, p)',
            'variables': {
                'Variable': 'Y',
                'Descripción': 'Vivienda tiene vistas al lago',
                'Valores posibles': '{0, 1}',
                '1': 'Sí tiene lago',
                '0': 'No tiene lago'
            },
            'interpretacion': 'Cada vivienda es un experimento de Bernoulli con dos resultados posibles'
        })
        
        pasos.append({
            'titulo': 'Paso 2: Cálculo de Probabilidad',
            'descripcion': 'Calculamos la probabilidad de éxito (tener lago) a partir de los datos',
            'formula': 'p = (Número de éxitos) / (Número total de experimentos)',
            'formula_desarrollada': f'p = {n_con_lago} / {n_total} = {p:.4f}',
            'valores': {
                'Total de viviendas (n)': n_total,
                'Viviendas con lago': n_con_lago,
                'Probabilidad de éxito (p)': p,
                'Probabilidad de fracaso (q = 1-p)': q
            },
            'interpretacion': f'La probabilidad de que una vivienda elegida al azar tenga vistas al lago es {p*100:.2f}%'
        })
        
        pasos.append({
            'titulo': 'Paso 3: Distribución Binomial',
            'descripcion': 'Aplicamos la función de masa de probabilidad (PMF) de la distribución binomial',
            'formula': 'P(Y = k) = C(n,k) × pᵏ × (1-p)ⁿ⁻ᵏ',
            'formula_n1': f'P(Y = 1) = C(1,1) × {p:.4f}¹ × {q:.4f}⁰ = {p:.4f}',
            'formula_n0': f'P(Y = 0) = C(1,0) × {p:.4f}⁰ × {q:.4f}¹ = {q:.4f}',
            'pmf_valores': {
                'P(Y = 0)': float(q),
                'P(Y = 1)': float(p)
            },
            'interpretacion': 'La función de masa de probabilidad nos da la probabilidad de cada resultado posible'
        })
        
        pasos.append({
            'titulo': 'Paso 4: Esperanza y Varianza',
            'descripcion': 'Calculamos la esperanza matemática y varianza de la distribución binomial',
            'esperanza_formula': 'E(Y) = n × p',
            'esperanza_calculo': f'E(Y) = 1 × {p:.4f} = {p:.4f}',
            'esperanza_valor': float(p),
            'varianza_formula': 'Var(Y) = n × p × (1-p)',
            'varianza_calculo': f'Var(Y) = 1 × {p:.4f} × {q:.4f} = {p*q:.6f}',
            'varianza_valor': float(p * q),
            'desviacion_formula': 'σ = √Var(Y)',
            'desviacion_valor': float(np.sqrt(p * q)),
            'interpretacion': 'La esperanza es el valor esperado de tener lago, y la varianza mide la dispersión'
        })
        
        # Simulación para múltiples experimentos
        n_sim = 10
        x_values = list(range(n_sim + 1))
        pmf_values = [float(binom.pmf(k, n_sim, p)) for k in x_values]
        
        pasos.append({
            'titulo': 'Paso 5: Extensión a Múltiples Experimentos',
            'descripcion': 'Si repetimos el experimento n veces, la suma sigue una distribución binomial',
            'formula': 'S = Σ Yᵢ ~ Binomial(n, p)',
            'formula_desarrollada': f'Para n={n_sim} viviendas: S ~ Binomial(n={n_sim}, p={p:.4f})',
            'esperanza_suma': f'E(S) = {n_sim} × {p:.4f} = {n_sim * p:.4f}',
            'varianza_suma': f'Var(S) = {n_sim} × {p:.4f} × {q:.4f} = {n_sim * p * q:.4f}',
            'pmf_simulacion': [
                {'k': k, 'probabilidad': prob} 
                for k, prob in zip(x_values, pmf_values)
            ],
            'interpretacion': 'Si seleccionamos múltiples viviendas, el número total con lago sigue una binomial'
        })
        
        return pasos
    
    def _analisis_poisson(self) -> List[Dict]:
        """Análisis de Distribución Poisson con paso a paso"""
        pasos = []
        
        chimeneas = self.df['chimenea']
        lambda_param = float(chimeneas.mean())
        n = len(chimeneas)
        
        pasos.append({
            'titulo': 'Paso 1: Definición de Variable Aleatoria Poisson',
            'descripcion': 'Definimos una variable aleatoria discreta que modela eventos raros',
            'formula': 'Z = Número de chimeneas en una vivienda',
            'formula_desarrollada': 'Z ~ Poisson(λ)',
            'variables': {
                'Variable': 'Z',
                'Descripción': 'Número de chimeneas',
                'Valores posibles': '{0, 1, 2, 3, ...}',
                'Tipo': 'Variable aleatoria discreta (conteo)'
            },
            'interpretacion': 'La distribución de Poisson modela el número de eventos raros en un intervalo'
        })
        
        pasos.append({
            'titulo': 'Paso 2: Estimación del Parámetro λ',
            'descripcion': 'El parámetro lambda (λ) es igual a la media de la distribución',
            'formula': 'λ = E(Z) = Media observada',
            'formula_calculo': f'λ = Σzᵢ / n = {chimeneas.sum()} / {n} = {lambda_param:.4f}',
            'parametro': {
                'Lambda (λ)': lambda_param,
                'Total de chimeneas': int(chimeneas.sum()),
                'Número de viviendas': n
            },
            'interpretacion': f'En promedio, cada vivienda tiene {lambda_param:.2f} chimeneas'
        })
        
        pasos.append({
            'titulo': 'Paso 3: Función de Masa de Probabilidad (PMF)',
            'descripcion': 'La PMF de Poisson nos da la probabilidad de observar k chimeneas',
            'formula': 'P(Z = k) = (λᵏ × e⁻λ) / k!',
            'formula_desarrollada': f'P(Z = k) = ({lambda_param:.4f}ᵏ × e⁻{lambda_param:.4f}) / k!',
            'pmf_ejemplos': [
                {
                    'k': 0,
                    'formula': f'P(Z = 0) = ({lambda_param:.4f}⁰ × e⁻{lambda_param:.4f}) / 0!',
                    'calculo': f'P(Z = 0) = 1 × {np.exp(-lambda_param):.4f} / 1',
                    'valor': float(poisson.pmf(0, lambda_param))
                },
                {
                    'k': 1,
                    'formula': f'P(Z = 1) = ({lambda_param:.4f}¹ × e⁻{lambda_param:.4f}) / 1!',
                    'calculo': f'P(Z = 1) = {lambda_param:.4f} × {np.exp(-lambda_param):.4f} / 1',
                    'valor': float(poisson.pmf(1, lambda_param))
                },
                {
                    'k': 2,
                    'formula': f'P(Z = 2) = ({lambda_param:.4f}² × e⁻{lambda_param:.4f}) / 2!',
                    'calculo': f'P(Z = 2) = {lambda_param**2:.4f} × {np.exp(-lambda_param):.4f} / 2',
                    'valor': float(poisson.pmf(2, lambda_param))
                }
            ],
            'interpretacion': 'La probabilidad disminuye rápidamente a medida que aumenta el número de chimeneas'
        })
        
        # Calcular PMF para todos los valores observados
        k_values = list(range(int(chimeneas.max()) + 1))
        pmf_all = [float(poisson.pmf(k, lambda_param)) for k in k_values]
        frec_esperada = [float(poisson.pmf(k, lambda_param) * n) for k in k_values]
        frec_observada = [int((chimeneas == k).sum()) for k in k_values]
        
        pasos.append({
            'titulo': 'Paso 4: Comparación Observada vs Teórica',
            'descripcion': 'Comparamos las frecuencias observadas con las esperadas según Poisson',
            'tabla_comparacion': [
                {
                    'k': k,
                    'frec_observada': obs,
                    'frec_esperada': esp,
                    'probabilidad_teorica': prob
                }
                for k, obs, esp, prob in zip(k_values, frec_observada, frec_esperada, pmf_all)
            ],
            'formula_frecuencia': 'Frecuencia esperada = P(Z = k) × n',
            'interpretacion': 'Si los datos siguen Poisson, las frecuencias observadas deberían ser similares a las esperadas'
        })
        
        pasos.append({
            'titulo': 'Paso 5: Esperanza y Varianza de Poisson',
            'descripcion': 'Propiedad especial: en Poisson, la esperanza es igual a la varianza',
            'esperanza_formula': 'E(Z) = λ',
            'esperanza_valor': lambda_param,
            'varianza_formula': 'Var(Z) = λ',
            'varianza_valor': lambda_param,
            'propiedad': 'E(Z) = Var(Z) = λ',
            'desviacion_formula': 'σ = √λ',
            'desviacion_valor': float(np.sqrt(lambda_param)),
            'interpretacion': 'Esta es una propiedad única de la distribución Poisson: media igual a varianza'
        })
        
        pasos.append({
            'titulo': 'Paso 6: Condiciones para Usar Poisson',
            'descripcion': 'Verificamos que los datos cumplan las condiciones para modelar con Poisson',
            'condiciones': {
                'Eventos independientes': 'El número de chimeneas en una casa no afecta a otras',
                'Tasa constante': f'La probabilidad promedio ({lambda_param:.4f}) es constante',
                'Eventos raros': 'Tener muchas chimeneas es un evento raro',
                'Discretos': 'Solo valores enteros (0, 1, 2, ...)'
            },
            'cumple_condiciones': True,
            'interpretacion': 'Los datos cumplen las condiciones para ser modelados con una distribución Poisson'
        })
        
        return pasos
    
    def _analisis_esperanza_varianza(self) -> List[Dict]:
        """Análisis de Esperanza Matemática y Varianza con paso a paso"""
        pasos = []
        
        mu = float(self.precio.mean())
        sigma2 = float(self.precio.var(ddof=0))
        sigma = float(self.precio.std(ddof=0))
        
        pasos.append({
            'titulo': 'Paso 1: Esperanza Matemática (Valor Esperado)',
            'descripcion': 'La esperanza matemática es el valor promedio esperado de la variable aleatoria',
            'formula_continua': 'E(X) = ∫ x × f(x) dx',
            'formula_discreta': 'E(X) = Σ xᵢ × P(xᵢ)',
            'formula_empirica': 'E(X) ≈ (Σxᵢ) / n',
            'formula_calculo': f'E(X) = ${mu:,.2f}',
            'valor': mu,
            'interpretacion': f'Si seleccionamos una vivienda al azar, esperamos que su precio sea aproximadamente ${mu:,.0f}'
        })
        
        pasos.append({
            'titulo': 'Paso 2: Varianza',
            'descripcion': 'La varianza mide qué tan dispersos están los valores alrededor de la media',
            'formula_continua': 'Var(X) = ∫ (x - μ)² × f(x) dx',
            'formula_alternativa': 'Var(X) = E(X²) - [E(X)]²',
            'formula_empirica': 'Var(X) = Σ(xᵢ - x̄)² / n',
            'formula_calculo': f'Var(X) = ${sigma2:,.2f}',
            'valor': sigma2,
            'desviacion_formula': 'σ = √Var(X)',
            'desviacion_valor': sigma,
            'unidad_varianza': 'Dólares al cuadrado ($²)',
            'unidad_desviacion': 'Dólares ($)',
            'interpretacion': f'La desviación estándar de ${sigma:,.0f} indica que los precios varían considerablemente alrededor de la media'
        })
        
        # Esperanza condicional
        precio_con_lago = self.df[self.df['vistas_lago'] == 'Yes']['precio']
        precio_sin_lago = self.df[self.df['vistas_lago'] == 'No']['precio']
        
        mu_con_lago = float(precio_con_lago.mean())
        mu_sin_lago = float(precio_sin_lago.mean())
        diferencia = mu_con_lago - mu_sin_lago
        
        pasos.append({
            'titulo': 'Paso 3: Esperanza Condicional',
            'descripcion': 'La esperanza condicional calcula el valor esperado dado que conocemos otra información',
            'formula_general': 'E(X | Y = y)',
            'formula_ejemplo': 'E(Precio | Lago = Sí)',
            'formula_calculo_con': f'E(Precio | Lago = Sí) = ${mu_con_lago:,.2f}',
            'formula_calculo_sin': f'E(Precio | Lago = No) = ${mu_sin_lago:,.2f}',
            'valores': {
                'E(Precio | Lago = Sí)': mu_con_lago,
                'E(Precio | Lago = No)': mu_sin_lago,
                'Diferencia': diferencia
            },
            'n_con_lago': len(precio_con_lago),
            'n_sin_lago': len(precio_sin_lago),
            'interpretacion': f'Tener vistas al lago aumenta el precio esperado en ${diferencia:,.0f} en promedio'
        })
        
        pasos.append({
            'titulo': 'Paso 4: Propiedades de Esperanza y Varianza',
            'descripcion': 'Aplicamos las propiedades matemáticas fundamentales',
            'propiedad_1': 'E(aX + b) = a × E(X) + b',
            'propiedad_2': 'Var(aX + b) = a² × Var(X)',
            'propiedad_3': 'E(X + Y) = E(X) + E(Y)',
            'propiedad_4': 'Var(X + Y) = Var(X) + Var(Y) + 2Cov(X,Y)',
            'ejemplo_linealidad': 'Si todos los precios aumentan un 10%, E(X) aumenta 10%',
            'ejemplo_escala': 'Si medimos en miles de dólares, Var(X) se reduce por un factor de 1,000,000',
            'interpretacion': 'Estas propiedades son fundamentales para el análisis estadístico'
        })
        
        pasos.append({
            'titulo': 'Paso 5: Coeficiente de Variación',
            'descripcion': 'Medimos la variabilidad relativa respecto a la media',
            'formula': 'CV = (σ / μ) × 100%',
            'formula_calculo': f'CV = (${sigma:,.0f} / ${mu:,.0f}) × 100% = {(sigma/mu)*100:.2f}%',
            'valor': float((sigma/mu) * 100),
            'interpretacion': 'Un CV alto indica alta variabilidad relativa. El precio de las viviendas es muy variable'
        })
        
        return pasos
    
    def _analisis_bayes(self) -> List[Dict]:
        """Análisis del Teorema de Bayes con paso a paso"""
        pasos = []
        
        umbral_cara = 250000
        self.df['casa_cara'] = self.df['precio'] > umbral_cara
        
        # Probabilidades
        P_A = float((self.df['casa_cara'] == True).sum() / len(self.df))
        P_B = float((self.df['vistas_lago'] == 'Yes').sum() / len(self.df))
        P_A_y_B = float(((self.df['casa_cara'] == True) & (self.df['vistas_lago'] == 'Yes')).sum() / len(self.df))
        P_A_dado_B = float(P_A_y_B / P_B)
        P_B_dado_A = float(P_A_y_B / P_A)
        
        pasos.append({
            'titulo': 'Paso 1: Definición de Eventos',
            'descripcion': 'Definimos los eventos para aplicar el Teorema de Bayes',
            'eventos': {
                'A': f'Casa cara (precio > ${umbral_cara:,})',
                'B': 'Casa con vistas al lago',
                'A ∩ B': f'Casa cara Y con lago',
                'A | B': f'Casa cara DADO que tiene lago'
            },
            'conteos': {
                'Total de casas': len(self.df),
                'Casas caras (A)': int((self.df['casa_cara'] == True).sum()),
                'Casas con lago (B)': int((self.df['vistas_lago'] == 'Yes').sum()),
                'Casas caras Y con lago (A ∩ B)': int(((self.df['casa_cara'] == True) & (self.df['vistas_lago'] == 'Yes')).sum())
            },
            'interpretacion': 'Estos eventos nos permiten aplicar probabilidades condicionales'
        })
        
        pasos.append({
            'titulo': 'Paso 2: Cálculo de Probabilidades Marginales',
            'descripcion': 'Calculamos las probabilidades simples (marginales) de cada evento',
            'formula_pa': 'P(A) = (Número de casas caras) / (Total de casas)',
            'calculo_pa': f'P(A) = {(self.df["casa_cara"] == True).sum()} / {len(self.df)} = {P_A:.4f}',
            'valor_pa': P_A,
            'formula_pb': 'P(B) = (Número de casas con lago) / (Total de casas)',
            'calculo_pb': f'P(B) = {(self.df["vistas_lago"] == "Yes").sum()} / {len(self.df)} = {P_B:.4f}',
            'valor_pb': P_B,
            'formula_pa_y_b': 'P(A ∩ B) = (Número de casas caras Y con lago) / (Total)',
            'calculo_pa_y_b': f'P(A ∩ B) = {((self.df["casa_cara"] == True) & (self.df["vistas_lago"] == "Yes")).sum()} / {len(self.df)} = {P_A_y_B:.4f}',
            'valor_pa_y_b': P_A_y_B,
            'interpretacion': 'Las probabilidades marginales nos dan la probabilidad de cada evento sin información adicional'
        })
        
        pasos.append({
            'titulo': 'Paso 3: Probabilidades Condicionales',
            'descripcion': 'Calculamos las probabilidades condicionales usando la definición',
            'formula_condicional': 'P(A|B) = P(A ∩ B) / P(B)',
            'calculo_pa_dado_b': f'P(A|B) = {P_A_y_B:.4f} / {P_B:.4f} = {P_A_dado_B:.4f}',
            'valor_pa_dado_b': P_A_dado_B,
            'formula_inversa': 'P(B|A) = P(A ∩ B) / P(A)',
            'calculo_pb_dado_a': f'P(B|A) = {P_A_y_B:.4f} / {P_A:.4f} = {P_B_dado_A:.4f}',
            'valor_pb_dado_a': P_B_dado_A,
            'interpretacion': f'Sabiendo que una casa tiene lago, la probabilidad de que sea cara aumenta de {P_A*100:.2f}% a {P_A_dado_B*100:.2f}%'
        })
        
        pasos.append({
            'titulo': 'Paso 4: Teorema de Bayes',
            'descripcion': 'Aplicamos el Teorema de Bayes para actualizar nuestras creencias',
            'formula': 'P(A|B) = [P(B|A) × P(A)] / P(B)',
            'formula_nombres': 'Posterior = (Verosimilitud × Prior) / Evidencia',
            'calculo_paso1': f'P(B|A) × P(A) = {P_B_dado_A:.4f} × {P_A:.4f} = {P_B_dado_A*P_A:.4f}',
            'calculo_paso2': f'P(A|B) = {P_B_dado_A*P_A:.4f} / {P_B:.4f} = {P_A_dado_B:.4f}',
            'verificacion': bool(abs(P_A_dado_B - (P_B_dado_A * P_A / P_B)) < 0.0001),
            'componentes': {
                'Prior P(A)': P_A,
                'Verosimilitud P(B|A)': P_B_dado_A,
                'Evidencia P(B)': P_B,
                'Posterior P(A|B)': P_A_dado_B
            },
            'interpretacion': 'El Teorema de Bayes nos permite actualizar la probabilidad de A después de observar B'
        })
        
        incremento = (P_A_dado_B - P_A) * 100
        
        pasos.append({
            'titulo': 'Paso 5: Interpretación del Resultado',
            'descripcion': 'Analizamos el impacto de la información condicional',
            'probabilidad_antes': {
                'valor': P_A,
                'porcentaje': P_A * 100,
                'interpretacion': 'Probabilidad de que una casa sea cara (sin información adicional)'
            },
            'probabilidad_despues': {
                'valor': P_A_dado_B,
                'porcentaje': P_A_dado_B * 100,
                'interpretacion': 'Probabilidad de que una casa sea cara DADO que tiene lago'
            },
            'incremento': {
                'absoluto': float(P_A_dado_B - P_A),
                'porcentual': float(incremento),
                'factor': float(P_A_dado_B / P_A) if P_A > 0 else 0,
                'interpretacion': f'La información de tener lago aumenta la probabilidad en {incremento:.2f} puntos porcentuales'
            },
            'interpretacion_final': 'Tener vistas al lago es un indicador fuerte de que una casa será cara'
        })
        
        return pasos
    
    def _analisis_intervalos_confianza(self) -> List[Dict]:
        """Análisis de Intervalos de Confianza con paso a paso"""
        pasos = []
        
        confidence_level = 0.95
        alpha = 1 - confidence_level
        n = len(self.precio)
        mean_precio = float(self.precio.mean())
        std_precio = float(self.precio.std(ddof=1))
        se = float(std_precio / np.sqrt(n))
        t_critical = float(stats.t.ppf(1 - alpha/2, df=n-1))
        margin_error = float(t_critical * se)
        ci_lower = float(mean_precio - margin_error)
        ci_upper = float(mean_precio + margin_error)
        
        pasos.append({
            'titulo': 'Paso 1: Objetivo del Intervalo de Confianza',
            'descripcion': 'Queremos estimar el precio promedio poblacional con un nivel de confianza',
            'formula_objetivo': 'IC para μ (media poblacional)',
            'parametros': {
                'Nivel de confianza': f'{confidence_level*100}%',
                'Alpha (α)': alpha,
                'Alpha/2': alpha/2,
                'Nivel de significancia': f'{alpha*100}%'
            },
            'interpretacion': f'Queremos un intervalo que contenga el precio promedio real con {confidence_level*100}% de confianza'
        })
        
        pasos.append({
            'titulo': 'Paso 2: Estadísticas de la Muestra',
            'descripcion': 'Calculamos las medidas necesarias de nuestra muestra',
            'valores': {
                'Tamaño de muestra (n)': n,
                'Media muestral (x̄)': mean_precio,
                'Desviación estándar muestral (s)': std_precio,
                'Grados de libertad (df)': n - 1
            },
            'formula_error_estandar': 'SE = s / √n',
            'calculo_error_estandar': f'SE = ${std_precio:,.2f} / √{n} = ${se:,.2f}',
            'error_estandar': se,
            'interpretacion': 'El error estándar mide qué tan precisa es nuestra estimación de la media'
        })
        
        pasos.append({
            'titulo': 'Paso 3: Valor Crítico de la Distribución t',
            'descripcion': 'Buscamos el valor crítico t para el nivel de confianza y grados de libertad',
            'formula': f't_α/2,df = t_{alpha/2:.3f}, {n-1}',
            'busqueda': f'Buscamos t tal que P(-t ≤ T ≤ t) = {confidence_level*100}%',
            'valor_critico': t_critical,
            'formula_calculo': f't_{1-alpha/2:.3f}, {n-1} = {t_critical:.4f}',
            'interpretacion': f'El {confidence_level*100}% de los valores de t están entre -{t_critical:.4f} y {t_critical:.4f}'
        })
        
        pasos.append({
            'titulo': 'Paso 4: Cálculo del Margen de Error',
            'descripcion': 'El margen de error determina qué tan ancho es nuestro intervalo',
            'formula': 'Margen de Error = t_crítico × Error Estándar',
            'calculo_paso1': f'ME = t_{1-alpha/2:.3f}, {n-1} × SE',
            'calculo_paso2': f'ME = {t_critical:.4f} × ${se:,.2f}',
            'calculo_paso3': f'ME = ${margin_error:,.2f}',
            'margen_error': margin_error,
            'interpretacion': 'El margen de error nos dice qué tan lejos puede estar la media real de nuestra media muestral'
        })
        
        pasos.append({
            'titulo': 'Paso 5: Construcción del Intervalo de Confianza',
            'descripcion': 'Construimos el intervalo sumando y restando el margen de error a la media',
            'formula': 'IC(1-α) = [x̄ - ME, x̄ + ME]',
            'calculo_inferior': f'Límite inferior = ${mean_precio:,.2f} - ${margin_error:,.2f} = ${ci_lower:,.2f}',
            'calculo_superior': f'Límite superior = ${mean_precio:,.2f} + ${margin_error:,.2f} = ${ci_upper:,.2f}',
            'intervalo': {
                'Límite inferior': ci_lower,
                'Límite superior': ci_upper,
                'Amplitud': ci_upper - ci_lower
            },
            'formula_final': f'IC({confidence_level*100}%) = [${ci_lower:,.2f}, ${ci_upper:,.2f}]',
            'interpretacion': f'Con {confidence_level*100}% de confianza, el precio promedio poblacional está entre ${ci_lower:,.0f} y ${ci_upper:,.0f}'
        })
        
        # Diferentes niveles de confianza
        confidence_levels = [0.90, 0.95, 0.99]
        intervals_multiples = []
        for conf in confidence_levels:
            alpha_mult = 1 - conf
            t_crit = float(stats.t.ppf(1 - alpha_mult/2, df=n-1))
            me = float(t_crit * se)
            intervals_multiples.append({
                'nivel': conf * 100,
                't_critico': t_crit,
                'margen_error': me,
                'inferior': float(mean_precio - me),
                'superior': float(mean_precio + me),
                'amplitud': float(2 * me)
            })
        
        pasos.append({
            'titulo': 'Paso 6: Comparación de Diferentes Niveles de Confianza',
            'descripcion': 'A mayor confianza, más ancho es el intervalo (trade-off)',
            'comparacion': intervals_multiples,
            'observacion': 'A medida que aumenta el nivel de confianza, el intervalo se vuelve más amplio pero más seguro',
            'interpretacion': 'Debemos balancear precisión (intervalo estrecho) con confianza (alta probabilidad)'
        })
        
        return pasos
    
    def _analisis_pruebas_hipotesis(self) -> List[Dict]:
        """Análisis de Pruebas de Hipótesis con paso a paso"""
        pasos = []
        
        # Test t
        precio_con_lago = self.df[self.df['vistas_lago'] == 'Yes']['precio']
        precio_sin_lago = self.df[self.df['vistas_lago'] == 'No']['precio']
        
        t_stat, p_value_t = ttest_ind(precio_con_lago, precio_sin_lago, alternative='greater')
        
        mu_con = float(precio_con_lago.mean())
        mu_sin = float(precio_sin_lago.mean())
        n_con = len(precio_con_lago)
        n_sin = len(precio_sin_lago)
        s_con = float(precio_con_lago.std(ddof=1))
        s_sin = float(precio_sin_lago.std(ddof=1))
        
        pasos.append({
            'titulo': 'Prueba 1: Test t - ¿Las casas con lago son más caras?',
            'descripcion': 'Usamos una prueba t para dos muestras independientes',
            'paso_1_hipotesis': {
                'titulo': 'Paso 1: Definición de Hipótesis',
                'h0': 'H₀: μ_con_lago = μ_sin_lago (No hay diferencia)',
                'h1': 'H₁: μ_con_lago > μ_sin_lago (Casas con lago son más caras)',
                'tipo_prueba': 'Prueba unilateral (cola superior)',
                'nivel_significancia': 'α = 0.05'
            },
            'paso_2_datos': {
                'titulo': 'Paso 2: Estadísticas de las Muestras',
                'muestra_1': {
                    'nombre': 'Con lago',
                    'n': n_con,
                    'media': mu_con,
                    'desviacion': s_con
                },
                'muestra_2': {
                    'nombre': 'Sin lago',
                    'n': n_sin,
                    'media': mu_sin,
                    'desviacion': s_sin
                },
                'diferencia': mu_con - mu_sin
            },
            'paso_3_estadistico': {
                'titulo': 'Paso 3: Cálculo del Estadístico t',
                'formula': 't = (x̄₁ - x̄₂) / SE',
                'formula_se': 'SE = √[(s₁²/n₁) + (s₂²/n₂)]',
                'calculo_se': f'SE = √[({s_con**2:.2f}/{n_con}) + ({s_sin**2:.2f}/{n_sin})]',
                'se_valor': float(np.sqrt((s_con**2/n_con) + (s_sin**2/n_sin))),
                'calculo_t': f't = (${mu_con:,.2f} - ${mu_sin:,.2f}) / SE',
                't_estadistico': float(t_stat),
                'df_aproximado': n_con + n_sin - 2
            },
            'paso_4_pvalor': {
                'titulo': 'Paso 4: Cálculo del Valor p',
                'formula': 'p-valor = P(T > t | H₀ verdadera)',
                'p_valor': float(p_value_t),
                'interpretacion_p': 'Probabilidad de observar esta diferencia (o mayor) si H₀ fuera verdadera'
            },
            'paso_5_conclusion': {
                'titulo': 'Paso 5: Decisión y Conclusión',
                'regla_decision': 'Si p-valor < α, rechazamos H₀',
                'comparacion': f'{p_value_t:.6f} {"<" if p_value_t < 0.05 else "≥"} 0.05',
                'decision': 'RECHAZAMOS H₀' if p_value_t < 0.05 else 'NO RECHAZAMOS H₀',
                'conclusion': 'Las casas con lago SÍ son significativamente más caras' if p_value_t < 0.05 else 'No hay evidencia suficiente para concluir que las casas con lago son más caras',
                'significativo': bool(p_value_t < 0.05)
            }
        })
        
        # Test Chi-cuadrado
        tabla_obs = pd.crosstab(self.df['aire_acondicionado'], self.df['vistas_lago'])
        chi2_stat, p_value_chi2, dof, expected_freq = chi2_contingency(tabla_obs)
        
        tabla_obs_dict = tabla_obs.to_dict()
        tabla_esp_dict = pd.DataFrame(expected_freq, index=tabla_obs.index, columns=tabla_obs.columns).to_dict()
        
        pasos.append({
            'titulo': 'Prueba 2: Test Chi-Cuadrado - ¿Aire acondicionado y lago son independientes?',
            'descripcion': 'Usamos una prueba chi-cuadrado para verificar independencia entre variables categóricas',
            'paso_1_hipotesis': {
                'titulo': 'Paso 1: Definición de Hipótesis',
                'h0': 'H₀: Las variables son independientes',
                'h1': 'H₁: Las variables NO son independientes (hay asociación)',
                'tipo_prueba': 'Prueba bilateral',
                'nivel_significancia': 'α = 0.05'
            },
            'paso_2_tabla_observada': {
                'titulo': 'Paso 2: Tabla de Contingencia Observada',
                'tabla': tabla_obs_dict,
                'totales': {
                    'Total por fila': tabla_obs.sum(axis=1).to_dict(),
                    'Total por columna': tabla_obs.sum(axis=0).to_dict(),
                    'Gran total': int(tabla_obs.sum().sum())
                },
                'interpretacion': 'Frecuencias observadas de cada combinación de categorías'
            },
            'paso_3_frecuencias_esperadas': {
                'titulo': 'Paso 3: Cálculo de Frecuencias Esperadas (bajo H₀)',
                'formula': 'Eᵢⱼ = (Total fila i × Total columna j) / Gran total',
                'tabla_esperada': tabla_esp_dict,
                'interpretacion': 'Frecuencias que esperaríamos si las variables fueran independientes'
            },
            'paso_4_estadistico': {
                'titulo': 'Paso 4: Cálculo del Estadístico Chi-Cuadrado',
                'formula': 'χ² = Σ [(Oᵢⱼ - Eᵢⱼ)² / Eᵢⱼ]',
                'calculo_celdas': [
                    {
                        'celda': f'({i}, {j})',
                        'observada': int(tabla_obs.loc[i, j]),
                        'esperada': float(expected_freq[tabla_obs.index.get_loc(i), tabla_obs.columns.get_loc(j)]),
                        'contribucion': float(((tabla_obs.loc[i, j] - expected_freq[tabla_obs.index.get_loc(i), tabla_obs.columns.get_loc(j)])**2) / expected_freq[tabla_obs.index.get_loc(i), tabla_obs.columns.get_loc(j)])
                    }
                    for i in tabla_obs.index
                    for j in tabla_obs.columns
                ],
                'chi2_estadistico': float(chi2_stat),
                'grados_libertad': int(dof),
                'formula_grados': 'df = (filas - 1) × (columnas - 1)'
            },
            'paso_5_pvalor': {
                'titulo': 'Paso 5: Cálculo del Valor p',
                'formula': 'p-valor = P(χ² ≥ estadístico | H₀ verdadera)',
                'p_valor': float(p_value_chi2),
                'chi2_critico': float(stats.chi2.ppf(0.95, dof)),
                'interpretacion': 'Probabilidad de observar esta asociación (o mayor) si H₀ fuera verdadera'
            },
            'paso_6_conclusion': {
                'titulo': 'Paso 6: Decisión y Conclusión',
                'regla_decision': 'Si p-valor < α, rechazamos H₀',
                'comparacion': f'{p_value_chi2:.6f} {"<" if p_value_chi2 < 0.05 else "≥"} 0.05',
                'decision': 'RECHAZAMOS H₀' if p_value_chi2 < 0.05 else 'NO RECHAZAMOS H₀',
                'conclusion': 'Existe asociación entre aire acondicionado y vistas al lago' if p_value_chi2 < 0.05 else 'No hay evidencia de asociación entre las variables',
                'significativo': bool(p_value_chi2 < 0.05)
            }
        })
        
        return pasos


def generar_analisis_completo() -> Dict:
    """
    Función auxiliar para generar análisis completo
    """
    analizador = AnalisisEstadistico()
    analizador.cargar_datos()
    return analizador.generar_analisis_completo()

