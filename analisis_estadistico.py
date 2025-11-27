#!/usr/bin/env python3
"""
ANALISIS ESTADISTICO COMPLETO DE PRECIOS DE VIVIENDAS
==========================================================
Proyecto de Probabilidad y Estadistica

Este script realiza un analisis estadistico exhaustivo que incluye:
1. Distribuciones de probabilidad (Normal, Binomial, Poisson)
2. Teorema de Bayes y probabilidades condicionales
3. Pruebas de hipotesis (t-test, chi-cuadrado)
4. Intervalos de confianza
5. Esperanza matematica y varianza
6. Regresion lineal multiple con inferencia estadistica

Dataset: Saratoga Houses (1,728 viviendas)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, binom, poisson, chi2_contingency, ttest_ind, shapiro
import statsmodels.api as sm
import warnings
import os
warnings.filterwarnings('ignore')

# Crear directorio para gráficas
os.makedirs('graficas_estadisticas', exist_ok=True)

# Configuración de gráficas
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

print("="*80)
print("ANALISIS ESTADISTICO DE PRECIOS DE VIVIENDAS")
print("="*80)

# ============================================================================
# CARGA Y EXPLORACION DE DATOS
# ============================================================================
print("\n\n" + "="*80)
print("CARGA Y EXPLORACION DE DATOS")
print("="*80)

df = pd.read_csv('data/SaratogaHouses.csv')

print(f"\nTotal de observaciones: {len(df)}")
print(f"Total de variables: {df.shape[1]}")
print(f"\nVariables: {', '.join(df.columns.tolist())}")
print(f"\nEstadisticas Descriptivas del Precio:")
print(df['precio'].describe())

# ============================================================================
# VARIABLES ALEATORIAS Y DISTRIBUCIONES
# ============================================================================
print("\n\n" + "="*80)
print("VARIABLES ALEATORIAS Y DISTRIBUCIONES DE PROBABILIDAD")
print("="*80)

precio = df['precio']

print(f"\nVARIABLE ALEATORIA: X = PRECIO DE LA VIVIENDA")
print(f"\nTamano de la muestra (n): {len(precio)}")
print(f"\nMedidas de Tendencia Central:")
print(f"  Media (mu): ${precio.mean():,.2f}")
print(f"  Mediana: ${precio.median():,.2f}")
print(f"  Moda: ${precio.mode()[0]:,.2f}")
print(f"\nMedidas de Dispersion:")
print(f"  Varianza (sigma^2): ${precio.var():,.2f}")
print(f"  Desviacion Estandar (sigma): ${precio.std():,.2f}")
print(f"  Rango: ${precio.max() - precio.min():,.2f}")
print(f"\nForma de la Distribucion:")
print(f"  Asimetria (Skewness): {precio.skew():.4f}")
print(f"  Curtosis: {precio.kurtosis():.4f}")

# Test de Normalidad
statistic, p_value_norm = shapiro(precio)
print(f"\nTEST DE NORMALIDAD (Shapiro-Wilk)")
print(f"  Estadistico: {statistic:.6f}")
print(f"  P-valor: {p_value_norm:.6f}")
if p_value_norm > 0.05:
    print(f"  Los datos siguen una distribucion normal (p > 0.05)")
else:
    print(f"  Los datos no son perfectamente normales, pero con n > 30,")
    print(f"     por el Teorema del Limite Central, la media muestral si lo es.")

# Gráfica: Distribución Normal
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

mu = precio.mean()
sigma = precio.std()

axes[0].hist(precio, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
x = np.linspace(precio.min(), precio.max(), 100)
axes[0].plot(x, norm.pdf(x, mu, sigma), 'r-', linewidth=2, label=f'Normal(μ={mu:.0f}, σ={sigma:.0f})')
axes[0].axvline(mu, color='green', linestyle='--', linewidth=2, label=f'Media = ${mu:,.0f}')
axes[0].set_xlabel('Precio ($)', fontsize=12)
axes[0].set_ylabel('Densidad de Probabilidad', fontsize=12)
axes[0].set_title('Distribución del Precio con Curva Normal Teórica', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

stats.probplot(precio, dist="norm", plot=axes[1])
axes[1].set_title('Q-Q Plot', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficas_estadisticas/01_distribucion_normal.png', bbox_inches='tight')
plt.close()
print("\n✅ Gráfica guardada: graficas_estadisticas/01_distribucion_normal.png")

# Distribución Binomial: Vistas al Lago
print(f"\n🌊 DISTRIBUCIÓN BINOMIAL: Y = VIVIENDA CON VISTAS AL LAGO")
tiene_lago = (df['vistas_lago'] == 'Yes').astype(int)
n_total = len(tiene_lago)
n_con_lago = tiene_lago.sum()
p = n_con_lago / n_total

print(f"  Total de viviendas: {n_total}")
print(f"  Viviendas con lago: {n_con_lago}")
print(f"  Probabilidad (p): {p:.4f}")
print(f"  Y ~ Binomial(n=1, p={p:.4f})")
print(f"  E(Y) = {p:.4f}, Var(Y) = {p*(1-p):.6f}")

n_sim = 10
x_values = np.arange(0, n_sim + 1)
pmf_values = binom.pmf(x_values, n_sim, p)

plt.figure(figsize=(10, 6))
plt.bar(x_values, pmf_values, color='teal', alpha=0.7, edgecolor='black')
plt.xlabel('Número de viviendas con lago (k)', fontsize=12)
plt.ylabel('Probabilidad P(X = k)', fontsize=12)
plt.title(f'Distribución Binomial: X ~ Bin(n={n_sim}, p={p:.4f})', fontsize=14, fontweight='bold')
plt.xticks(x_values)
plt.grid(True, alpha=0.3, axis='y')
for i, v in enumerate(pmf_values):
    plt.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('graficas_estadisticas/02_binomial.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/02_binomial.png")

# Distribución de Poisson: Chimeneas
print(f"\n🔥 DISTRIBUCIÓN DE POISSON: Z = NÚMERO DE CHIMENEAS")
chimeneas = df['chimenea']
lambda_param = chimeneas.mean()

print(f"  Parámetro λ: {lambda_param:.4f}")
print(f"  Z ~ Poisson(λ={lambda_param:.4f})")
print(f"  E(Z) = Var(Z) = {lambda_param:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

chimeneas.value_counts().sort_index().plot(kind='bar', ax=axes[0], color='coral', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Número de Chimeneas', fontsize=12)
axes[0].set_ylabel('Frecuencia', fontsize=12)
axes[0].set_title('Distribución Observada', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)

k_values = np.arange(0, chimeneas.max() + 1)
pmf_poisson = poisson.pmf(k_values, lambda_param) * len(chimeneas)
axes[1].bar(k_values, pmf_poisson, color='darkorange', alpha=0.7, edgecolor='black')
axes[1].set_xlabel('Número de Chimeneas (k)', fontsize=12)
axes[1].set_ylabel('Frecuencia Esperada', fontsize=12)
axes[1].set_title(f'Distribución Teórica Poisson(λ={lambda_param:.2f})', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('graficas_estadisticas/03_poisson.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/03_poisson.png")

# ============================================================================
# 3️⃣ ESPERANZA MATEMÁTICA Y VARIANZA
# ============================================================================
print("\n\n" + "="*80)
print("3️⃣ ESPERANZA MATEMÁTICA Y VARIANZA")
print("="*80)

print(f"\n📊 Variable: X = Precio de la vivienda")
print(f"\n🎯 Esperanza Matemática: E(X) = μ = ${precio.mean():,.2f}")
print(f"📏 Varianza Poblacional: Var(X) = σ² = ${precio.var(ddof=0):,.2f}")
print(f"📐 Desviación Estándar: σ = ${precio.std(ddof=0):,.2f}")

# Esperanza Condicional
precio_con_lago = df[df['vistas_lago'] == 'Yes']['precio']
precio_sin_lago = df[df['vistas_lago'] == 'No']['precio']

print(f"\n🌊 ESPERANZA CONDICIONAL:")
print(f"  E(Precio | Lago = Sí):  ${precio_con_lago.mean():,.2f}")
print(f"  E(Precio | Lago = No):   ${precio_sin_lago.mean():,.2f}")
print(f"  Diferencia: ${precio_con_lago.mean() - precio_sin_lago.mean():,.2f}")

fig, ax = plt.subplots(figsize=(10, 6))
data_to_plot = [precio_sin_lago, precio_con_lago]
box = ax.boxplot(data_to_plot, labels=['Sin Lago', 'Con Lago'], patch_artist=True,
                 boxprops=dict(facecolor='lightblue', alpha=0.7),
                 medianprops=dict(color='red', linewidth=2))

means = [precio_sin_lago.mean(), precio_con_lago.mean()]
ax.plot([1, 2], means, 'D', color='green', markersize=12, label='Media (Esperanza)', zorder=3)
ax.set_ylabel('Precio ($)', fontsize=12)
ax.set_title('Comparación de Esperanzas Condicionales', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
ax.legend()
ax.text(1, means[0], f'${means[0]:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.text(2, means[1], f'${means[1]:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('graficas_estadisticas/04_esperanza_condicional.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/04_esperanza_condicional.png")

# ============================================================================
# 4️⃣ PROBABILIDADES CONDICIONALES Y TEOREMA DE BAYES
# ============================================================================
print("\n\n" + "="*80)
print("4️⃣ PROBABILIDADES CONDICIONALES Y TEOREMA DE BAYES")
print("="*80)

umbral_cara = 250000
df['casa_cara'] = df['precio'] > umbral_cara

# Probabilidades
P_A = (df['casa_cara'] == True).sum() / len(df)
P_B = (df['vistas_lago'] == 'Yes').sum() / len(df)
P_A_y_B = ((df['casa_cara'] == True) & (df['vistas_lago'] == 'Yes')).sum() / len(df)
P_A_dado_B = P_A_y_B / P_B
P_B_dado_A = P_A_y_B / P_A

print(f"\n🎲 Eventos:")
print(f"  A: Casa cara (precio > ${umbral_cara:,})")
print(f"  B: Casa con vistas al lago")
print(f"\n📊 Probabilidades:")
print(f"  P(A) = {P_A:.4f} ({P_A*100:.2f}%)")
print(f"  P(B) = {P_B:.4f} ({P_B*100:.2f}%)")
print(f"  P(A ∩ B) = {P_A_y_B:.4f} ({P_A_y_B*100:.2f}%)")
print(f"\n➡️ Probabilidades Condicionales:")
print(f"  P(A|B) = {P_A_dado_B:.4f} ({P_A_dado_B*100:.2f}%)")
print(f"  P(B|A) = {P_B_dado_A:.4f} ({P_B_dado_A*100:.2f}%)")

print(f"\n🎯 TEOREMA DE BAYES:")
print(f"  P(A|B) = [P(B|A) · P(A)] / P(B)")
print(f"  P(A|B) = [{P_B_dado_A:.4f} × {P_A:.4f}] / {P_B:.4f} = {P_A_dado_B:.4f} ✓")
print(f"\n💡 Interpretación:")
print(f"  Sabiendo que una casa tiene lago, la probabilidad de que sea cara")
print(f"  aumenta de {P_A*100:.2f}% a {P_A_dado_B*100:.2f}% (+{(P_A_dado_B-P_A)*100:.2f} puntos)")

# Tabla de contingencia
tabla_contingencia = pd.crosstab(df['casa_cara'], df['vistas_lago'])

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

tabla_contingencia.plot(kind='bar', ax=axes[0], color=['lightcoral', 'lightblue'], edgecolor='black')
axes[0].set_xlabel('Casa Cara', fontsize=12)
axes[0].set_ylabel('Frecuencia', fontsize=12)
axes[0].set_title('Precio vs Vistas al Lago', fontsize=14, fontweight='bold')
axes[0].set_xticklabels(['No', 'Sí'], rotation=0)
axes[0].legend(title='Lago')
axes[0].grid(True, alpha=0.3, axis='y')

probs = [P_A, P_A_dado_B]
labels = ['P(Cara)', 'P(Cara|Lago)']
bars = axes[1].bar(labels, probs, color=['steelblue', 'darkgreen'], alpha=0.7, edgecolor='black')
axes[1].set_ylabel('Probabilidad', fontsize=12)
axes[1].set_title('Teorema de Bayes: Actualización de Probabilidad', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')
for bar, prob in zip(bars, probs):
    axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{prob:.4f}\\n({prob*100:.2f}%)', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('graficas_estadisticas/05_bayes.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/05_bayes.png")

# ============================================================================
# 5️⃣ INTERVALOS DE CONFIANZA
# ============================================================================
print("\n\n" + "="*80)
print("5️⃣ INTERVALOS DE CONFIANZA")
print("="*80)

confidence_level = 0.95
alpha = 1 - confidence_level
n = len(precio)
mean_precio = precio.mean()
std_precio = precio.std(ddof=1)
se = std_precio / np.sqrt(n)
t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
margin_error = t_critical * se
ci_lower = mean_precio - margin_error
ci_upper = mean_precio + margin_error

print(f"\n📊 INTERVALO DE CONFIANZA DEL {confidence_level*100}%:")
print(f"  Nivel de confianza: {confidence_level*100}%")
print(f"  Tamaño de muestra: {n}")
print(f"  Media muestral: ${mean_precio:,.2f}")
print(f"  Error estándar: ${se:,.2f}")
print(f"  Valor t crítico: {t_critical:.4f}")
print(f"  Margen de error: ${margin_error:,.2f}")
print(f"\n🎯 INTERVALO: [${ci_lower:,.2f}, ${ci_upper:,.2f}]")
print(f"\n💡 Con {confidence_level*100}% de confianza, el precio promedio real")
print(f"   está entre ${ci_lower:,.2f} y ${ci_upper:,.2f}")

# Diferentes niveles de confianza
confidence_levels = [0.90, 0.95, 0.99]
intervals = []
for conf in confidence_levels:
    t_crit = stats.t.ppf(1 - (1-conf)/2, df=n-1)
    me = t_crit * se
    intervals.append((mean_precio - me, mean_precio + me))

fig, ax = plt.subplots(figsize=(12, 6))
y_positions = range(len(confidence_levels))
colors_ci = ['lightgreen', 'lightblue', 'lightcoral']

for i, (conf, interval, color) in enumerate(zip(confidence_levels, intervals, colors_ci)):
    lower, upper = interval
    ax.plot([lower, upper], [i, i], 'o-', linewidth=3, markersize=8, color=color)
    ax.fill_between([lower, upper], i-0.15, i+0.15, alpha=0.3, color=color)
    ax.text(lower, i+0.25, f'${lower:,.0f}', ha='center', va='bottom', fontsize=9)
    ax.text(upper, i+0.25, f'${upper:,.0f}', ha='center', va='bottom', fontsize=9)
    ax.text(mean_precio, i-0.25, f'{conf*100}%', ha='center', va='top', fontsize=10, fontweight='bold')

ax.axvline(mean_precio, color='red', linestyle='--', linewidth=2, label=f'Media = ${mean_precio:,.0f}')
ax.set_yticks(y_positions)
ax.set_yticklabels([f'{c*100}%' for c in confidence_levels])
ax.set_xlabel('Precio ($)', fontsize=12)
ax.set_ylabel('Nivel de Confianza', fontsize=12)
ax.set_title('Intervalos de Confianza para el Precio Medio', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('graficas_estadisticas/06_intervalos_confianza.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/06_intervalos_confianza.png")

# ============================================================================
# 6️⃣ PRUEBAS DE HIPÓTESIS
# ============================================================================
print("\n\n" + "="*80)
print("6️⃣ PRUEBAS DE HIPÓTESIS")
print("="*80)

# Test t
print(f"\n🔬 TEST T: ¿Las casas con lago son más caras?")
t_stat, p_value_t = ttest_ind(precio_con_lago, precio_sin_lago, alternative='greater')

print(f"  H₀: μ_con_lago = μ_sin_lago")
print(f"  H₁: μ_con_lago > μ_sin_lago")
print(f"\n  Con lago:   n={len(precio_con_lago)}, x̄=${precio_con_lago.mean():,.2f}")
print(f"  Sin lago:   n={len(precio_sin_lago)}, x̄=${precio_sin_lago.mean():,.2f}")
print(f"  Diferencia: ${precio_con_lago.mean() - precio_sin_lago.mean():,.2f}")
print(f"\n  Estadístico t: {t_stat:.4f}")
print(f"  Valor p: {p_value_t:.6f}")
if p_value_t < 0.05:
    print(f"  ✅ RECHAZAMOS H₀: Las casas con lago SÍ son más caras (p < 0.05)")
else:
    print(f"  ❌ NO RECHAZAMOS H₀: No hay diferencia significativa (p >= 0.05)")

# Test Chi-Cuadrado
print(f"\n🔬 TEST CHI-CUADRADO: ¿Aire acondicionado y lago son independientes?")
tabla_obs = pd.crosstab(df['aire_acondicionado'], df['vistas_lago'])
chi2_stat, p_value_chi2, dof, expected_freq = chi2_contingency(tabla_obs)

print(f"  H₀: Las variables son independientes")
print(f"  H₁: Las variables NO son independientes")
print(f"\n  Estadístico χ²: {chi2_stat:.4f}")
print(f"  Grados de libertad: {dof}")
print(f"  Valor p: {p_value_chi2:.6f}")
if p_value_chi2 < 0.05:
    print(f"  ✅ RECHAZAMOS H₀: Existe asociación (p < 0.05)")
else:
    print(f"  ❌ NO RECHAZAMOS H₀: Son independientes (p >= 0.05)")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

axes[0].hist(precio_sin_lago, bins=30, alpha=0.6, label='Sin Lago', color='coral', edgecolor='black')
axes[0].hist(precio_con_lago, bins=30, alpha=0.6, label='Con Lago', color='skyblue', edgecolor='black')
axes[0].axvline(precio_sin_lago.mean(), color='red', linestyle='--', linewidth=2)
axes[0].axvline(precio_con_lago.mean(), color='blue', linestyle='--', linewidth=2)
axes[0].set_xlabel('Precio ($)', fontsize=12)
axes[0].set_ylabel('Frecuencia', fontsize=12)
axes[0].set_title(f'Test t\\np-valor = {p_value_t:.6f}', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

tabla_prop = tabla_obs.div(tabla_obs.sum(axis=1), axis=0) * 100
sns.heatmap(tabla_prop, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1], linewidths=1, linecolor='black')
axes[1].set_title(f'Test χ²\\np-valor = {p_value_chi2:.6f}', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('graficas_estadisticas/07_pruebas_hipotesis.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/07_pruebas_hipotesis.png")

# ============================================================================
# 7️⃣ REGRESIÓN LINEAL MÚLTIPLE
# ============================================================================
print("\n\n" + "="*80)
print("7️⃣ REGRESIÓN LINEAL MÚLTIPLE (ESTADÍSTICA CLÁSICA)")
print("="*80)

vars_numericas = ['metros_habitables', 'metros_totales', 'antiguedad', 'precio_terreno', 
                  'dormitorios', 'banyos', 'habitaciones', 'chimenea', 'universitarios']

df_modelo = df.copy()
df_modelo['tiene_lago'] = (df_modelo['vistas_lago'] == 'Yes').astype(int)
df_modelo['tiene_aire'] = (df_modelo['aire_acondicionado'] == 'Yes').astype(int)
df_modelo['es_nueva'] = (df_modelo['nueva_construccion'] == 'Yes').astype(int)

vars_modelo = vars_numericas + ['tiene_lago', 'tiene_aire', 'es_nueva']

X = df_modelo[vars_modelo]
y = df_modelo['precio']
X = sm.add_constant(X)

modelo_ols = sm.OLS(y, X).fit()

print(f"\n📐 Modelo: Precio = β₀ + β₁·X₁ + β₂·X₂ + ... + ε")
print(f"\n📊 Métricas:")
print(f"  R²: {modelo_ols.rsquared:.4f} ({modelo_ols.rsquared*100:.2f}%)")
print(f"  R² Ajustado: {modelo_ols.rsquared_adj:.4f}")
print(f"  RMSE: ${np.sqrt(modelo_ols.mse_resid):,.2f}")

print(f"\n🔢 Coeficientes Significativos (p < 0.05):")
coeficientes = modelo_ols.params
p_values = modelo_ols.pvalues
for var in coeficientes.index:
    if p_values[var] < 0.05 and var != 'const':
        print(f"  {var:25s}: β = {coeficientes[var]:>10.2f} (p = {p_values[var]:.4f})")

# Guardar modelo OLS
import pickle
os.makedirs('model', exist_ok=True)
with open('model/modelo_regresion_lineal.pkl', 'wb') as f:
    pickle.dump(modelo_ols, f)
with open('model/variables_modelo.pkl', 'wb') as f:
    pickle.dump(vars_modelo, f)

# ============================================================================
# 8️⃣ REGRESIÓN BAYESIANA (Teorema de Bayes Aplicado)
# ============================================================================
print("\n\n" + "="*80)
print("8️⃣ REGRESIÓN BAYESIANA (Teorema de Bayes Aplicado a Predicción)")
print("="*80)

# Importar módulo de regresión bayesiana
from model.regresion_bayesiana import ModeloRegresionBayesiana

print("\n📊 Entrenando Modelo de Regresión Bayesiana...")
print("   Este modelo aplica el Teorema de Bayes para estimar coeficientes")

modelo_bayesiano = ModeloRegresionBayesiana()
metricas_bayesiano = modelo_bayesiano.entrenar(df)

print(f"\n📊 Métricas del Modelo Bayesiano:")
print(f"  R²: {metricas_bayesiano['r2']:.4f} ({metricas_bayesiano['r2']*100:.2f}%)")
print(f"  RMSE: ${metricas_bayesiano['rmse']:,.2f}")

# Guardar modelo bayesiano
modelo_bayesiano.guardar()

print(f"\n✅ Modelo Bayesiano entrenado y guardado")
print(f"   Comparación:")
print(f"   OLS (Frecuentista):     R² = {modelo_ols.rsquared:.4f}, RMSE = ${np.sqrt(modelo_ols.mse_resid):,.2f}")
print(f"   Bayesiano:              R² = {metricas_bayesiano['r2']:.4f}, RMSE = ${metricas_bayesiano['rmse']:,.2f}")
print(f"\n💡 Nota: Con prior no informativo, ambos modelos dan resultados similares.")
print(f"   La diferencia está en la interpretación estadística y la metodología.")

# Gráficas de residuos
residuos = modelo_ols.resid
predicciones = modelo_ols.fittedvalues

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

axes[0, 0].scatter(predicciones, residuos, alpha=0.5, s=20)
axes[0, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Valores Predichos')
axes[0, 0].set_ylabel('Residuos')
axes[0, 0].set_title('Residuos vs Predicciones', fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(residuos, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 1].axvline(x=0, color='r', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('Residuos')
axes[0, 1].set_ylabel('Frecuencia')
axes[0, 1].set_title('Distribución de Residuos', fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')

stats.probplot(residuos, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title('Q-Q Plot de Residuos', fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].scatter(y, predicciones, alpha=0.5, s=20)
axes[1, 1].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2, label='Línea ideal')
axes[1, 1].set_xlabel('Valores Reales')
axes[1, 1].set_ylabel('Valores Predichos')
axes[1, 1].set_title('Real vs Predicho', fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficas_estadisticas/08_regresion_residuos.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/08_regresion_residuos.png")

# Matriz de correlación
variables_para_corr = ['precio'] + vars_modelo
matriz_corr = df_modelo[variables_para_corr].corr()

plt.figure(figsize=(14, 12))
sns.heatmap(matriz_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlación de Pearson', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('graficas_estadisticas/09_correlacion.png', bbox_inches='tight')
plt.close()
print("✅ Gráfica guardada: graficas_estadisticas/09_correlacion.png")

# ============================================================================
# 8️⃣ CONCLUSIONES
# ============================================================================
print("\n\n" + "="*80)
print("📊 CONCLUSIONES DEL ANÁLISIS ESTADÍSTICO")
print("="*80)

print(f"\n1️⃣ DISTRIBUCIONES:")
print(f"   • Precio ~ Normal(μ=${precio.mean():,.0f}, σ=${precio.std():,.0f})")
print(f"   • Vistas lago ~ Binomial(p={p:.4f})")
print(f"   • Chimeneas ~ Poisson(λ={lambda_param:.4f})")

print(f"\n2️⃣ ESPERANZA Y VARIANZA:")
print(f"   • E(Precio) = ${precio.mean():,.2f}")
print(f"   • Var(Precio) = ${precio.var(ddof=0):,.2f}")
print(f"   • E(Precio|Lago=Sí) = ${precio_con_lago.mean():,.2f}")

print(f"\n3️⃣ TEOREMA DE BAYES:")
print(f"   • P(Cara) = {P_A:.4f} → P(Cara|Lago) = {P_A_dado_B:.4f}")
print(f"   • Incremento: +{(P_A_dado_B-P_A)*100:.2f} puntos porcentuales")

print(f"\n4️⃣ INTERVALOS DE CONFIANZA:")
print(f"   • IC 95%: [${ci_lower:,.2f}, ${ci_upper:,.2f}]")

print(f"\n5️⃣ PRUEBAS DE HIPÓTESIS:")
if p_value_t < 0.05:
    print(f"   • Test t: Casas con lago SÍ son más caras (p={p_value_t:.6f})")
else:
    print(f"   • Test t: No hay diferencia significativa (p={p_value_t:.6f})")
    
if p_value_chi2 < 0.05:
    print(f"   • Test χ²: Aire y lago NO son independientes (p={p_value_chi2:.6f})")
else:
    print(f"   • Test χ²: Aire y lago son independientes (p={p_value_chi2:.6f})")

print(f"\n6️⃣ REGRESIÓN LINEAL:")
print(f"   • R² = {modelo_ols.rsquared:.4f} ({modelo_ols.rsquared*100:.2f}%)")
print(f"   • RMSE = ${np.sqrt(modelo_ols.mse_resid):,.2f}")

print("\n" + "="*80)
print("✅ ANÁLISIS COMPLETO FINALIZADO")
print("📁 Gráficas guardadas en: graficas_estadisticas/")
print("💾 Modelo guardado en: model/modelo_regresion_lineal.pkl")
print("="*80)

