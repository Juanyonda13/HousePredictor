"""
Aplicación Web para Predicción de Precios de Casas
Proyecto de Probabilidad y Estadística

Framework: Flask (Arquitectura Monolítica)
Modelo: Regresión Lineal Múltiple (OLS - Estadística Clásica)
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
import os
from model.regresion_lineal import ModeloRegresionLineal
from model.regresion_bayesiana import ModeloRegresionBayesiana
from model.analisis_distribuciones import AnalisisEstadistico


def convertir_numpy_a_nativo(obj):
    """
    Convierte recursivamente valores de NumPy a tipos nativos de Python
    para que sean JSON serializables
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convertir_numpy_a_nativo(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convertir_numpy_a_nativo(item) for item in obj]
    return obj

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Inicializar modelo de regresión lineal (OLS)
try:
    modelo_ols = ModeloRegresionLineal.cargar('model/modelo_regresion_lineal.pkl')
    print("✅ Modelo de Regresión Lineal (OLS) cargado exitosamente")
    print(f"   R² = {modelo_ols.modelo.rsquared:.4f} ({modelo_ols.modelo.rsquared*100:.2f}%)")
except FileNotFoundError as e:
    print(f"⚠️  Modelo OLS no encontrado. Ejecuta 'python3 analisis_estadistico.py' primero")
    modelo_ols = None

# Inicializar modelo de regresión bayesiana
try:
    modelo_bayes = ModeloRegresionBayesiana.cargar('model/modelo_regresion_bayesiana.pkl')
    print("✅ Modelo de Regresión Bayesiana cargado exitosamente")
    print(f"   R² = {modelo_bayes.modelo.rsquared:.4f} ({modelo_bayes.modelo.rsquared*100:.2f}%)")
    print(f"   Variables: {len(modelo_bayes.variables)} variables")
    print(f"   Modelo entrenado: {modelo_bayes.trained}")
except FileNotFoundError as e:
    print(f"⚠️  Modelo Bayesiano no encontrado. Ejecuta 'python3 analisis_estadistico.py' primero")
    print(f"   Archivo buscado: model/modelo_regresion_bayesiana.pkl")
    modelo_bayes = None
except Exception as e:
    print(f"⚠️  Error cargando modelo bayesiano: {str(e)}")
    import traceback
    traceback.print_exc()
    modelo_bayes = None


@app.route('/')
def index():
    """Página principal con formulario de predicción"""
    return render_template('index.html')


@app.route('/mapa')
def mapa():
    """Página con mapa interactivo de casas"""
    # Cargar datos de casas si existen
    casas_data = []
    if os.path.exists('data/SaratogaHouses.csv'):
        df = pd.read_csv('data/SaratogaHouses.csv')
        # Tomar una muestra para el mapa (para no saturar)
        df_sample = df.sample(n=min(100, len(df)), random_state=42)
        casas_data = df_sample.to_dict('records')
    
    return render_template('mapa.html', casas=json.dumps(casas_data))


@app.route('/analisis-estadistico')
def analisis_estadistico():
    """Página con análisis estadístico detallado paso a paso"""
    return render_template('analisis_estadistico.html')


@app.route('/api/predecir', methods=['POST'])
def api_predecir():
    """
    API endpoint para predecir precio de una casa
    
    Acepta JSON con las características de la casa
    Retorna JSON con predicciones de ambos modelos (OLS y Bayesiano)
    """
    if modelo_ols is None and modelo_bayes is None:
        return jsonify({
            'error': 'Modelos no disponibles. Ejecuta "python3 analisis_estadistico.py" primero.',
            'precio': None
        }), 500
    
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'error': 'No se recibieron datos',
                'precio': None
            }), 400
        
        # Verificar si se solicita paso a paso
        incluir_paso_a_paso = request.args.get('paso_a_paso', 'false').lower() == 'true'
        
        # Convertir valores numéricos
        campos_numericos = [
            'metros_totales', 'antiguedad', 'precio_terreno',
            'metros_habitables', 'universitarios', 'dormitorios',
            'chimenea', 'banyos', 'habitaciones'
        ]
        
        for campo in campos_numericos:
            if campo in datos:
                datos[campo] = float(datos[campo])
        
        response = {
            'error': None,
            'modelos': {}
        }
        
        print(f"\n{'='*60}")
        print(f"🔍 INICIO DE PREDICCIÓN")
        print(f"   modelo_ols cargado: {modelo_ols is not None}")
        print(f"   modelo_bayes cargado: {modelo_bayes is not None}")
        print(f"   incluir_paso_a_paso: {incluir_paso_a_paso}")
        print(f"{'='*60}\n")
        
        # Predicción con OLS (Frecuentista)
        if modelo_ols is not None:
            resultado_ols = modelo_ols.predecir(datos, incluir_paso_a_paso=incluir_paso_a_paso)
            response['modelos']['ols'] = {
                'precio': resultado_ols['precio_estimado'],
                'ic_inferior': resultado_ols['ic_inferior_95'],
                'ic_superior': resultado_ols['ic_superior_95'],
                'modelo': resultado_ols['modelo'],
                'r2': resultado_ols['r2'],
                'tipo': 'Frecuentista (OLS)',
                'intervalo_tipo': 'Intervalo de Confianza'
            }
            
            # Agregar paso a paso de OLS
            if incluir_paso_a_paso and 'paso_a_paso' in resultado_ols:
                response['modelos']['ols']['paso_a_paso'] = resultado_ols['paso_a_paso']
        
        # Predicción con Bayesiano
        print(f"\n🔍 DEBUG: modelo_bayes es None? {modelo_bayes is None}")
        print(f"🔍 DEBUG: incluir_paso_a_paso = {incluir_paso_a_paso}")
        
        if modelo_bayes is not None:
            print("🔍 DEBUG: Intentando predecir con modelo bayesiano...")
            try:
                resultado_bayes = modelo_bayes.predecir(datos, incluir_paso_a_paso=incluir_paso_a_paso)
                print(f"✅ Predicción bayesiana exitosa. Precio: ${resultado_bayes['precio_estimado']:,.2f}")
                
                response['modelos']['bayesiano'] = {
                    'precio': resultado_bayes['precio_estimado'],
                    'ic_inferior': resultado_bayes['ic_inferior_95'],
                    'ic_superior': resultado_bayes['ic_superior_95'],
                    'modelo': resultado_bayes['modelo'],
                    'r2': resultado_bayes['r2'],
                    'tipo': 'Bayesiano (Teorema de Bayes)',
                    'intervalo_tipo': resultado_bayes.get('tipo_intervalo', 'Intervalo Creíble')
                }
                
                # Agregar paso a paso bayesiano
                if incluir_paso_a_paso and 'paso_a_paso' in resultado_bayes:
                    response['modelos']['bayesiano']['paso_a_paso'] = resultado_bayes['paso_a_paso']
                    print(f"✅ Paso a paso bayesiano generado: {len(resultado_bayes['paso_a_paso'])} pasos")
                else:
                    print(f"⚠️  Paso a paso bayesiano no generado.")
                    print(f"   incluir_paso_a_paso = {incluir_paso_a_paso}")
                    print(f"   'paso_a_paso' en resultado_bayes = {'paso_a_paso' in resultado_bayes}")
                    if 'paso_a_paso' in resultado_bayes:
                        print(f"   Tipo de paso_a_paso: {type(resultado_bayes['paso_a_paso'])}")
            except Exception as e:
                print(f"❌ ERROR al predecir con modelo bayesiano: {str(e)}")
                import traceback
                traceback.print_exc()
                # No agregamos el modelo bayesiano si hay error, pero continuamos con OLS
        else:
            print("⚠️  Modelo bayesiano no está cargado (modelo_bayes es None)")
        
        print(f"🔍 DEBUG: response['modelos'] tiene: {list(response.get('modelos', {}).keys())}")
        print(f"🔍 DEBUG: JSON final antes de enviar:")
        print(f"   - OLS en response: {'ols' in response.get('modelos', {})}")
        print(f"   - Bayesiano en response: {'bayesiano' in response.get('modelos', {})}")
        
        # Por compatibilidad, usar OLS como precio principal si está disponible
        if modelo_ols is not None:
            response['precio'] = response['modelos']['ols']['precio']
            response['ic_inferior'] = response['modelos']['ols']['ic_inferior']
            response['ic_superior'] = response['modelos']['ols']['ic_superior']
            response['modelo'] = response['modelos']['ols']['modelo']
            response['r2'] = response['modelos']['ols']['r2']
        elif modelo_bayes is not None:
            response['precio'] = response['modelos']['bayesiano']['precio']
            response['ic_inferior'] = response['modelos']['bayesiano']['ic_inferior']
            response['ic_superior'] = response['modelos']['bayesiano']['ic_superior']
            response['modelo'] = response['modelos']['bayesiano']['modelo']
            response['r2'] = response['modelos']['bayesiano']['r2']
        
        # Log final antes de enviar
        print(f"\n{'='*60}")
        print(f"📤 ENVIANDO RESPUESTA")
        print(f"   Modelos en response: {list(response.get('modelos', {}).keys())}")
        if 'bayesiano' in response.get('modelos', {}):
            bayes_data = response['modelos']['bayesiano']
            print(f"   ✅ Bayesiano incluido: precio=${bayes_data.get('precio', 'N/A'):,.2f}")
            print(f"      Paso a paso: {'paso_a_paso' in bayes_data}")
        else:
            print(f"   ❌ Bayesiano NO incluido en response")
        print(f"{'='*60}\n")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"\n❌❌❌ ERROR GENERAL EN PREDICCIÓN ❌❌❌")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"❌❌❌ FIN DEL ERROR ❌❌❌\n")
        return jsonify({
            'error': f'Error en la predicción: {str(e)}',
            'precio': None
        }), 500


@app.route('/api/status-modelos', methods=['GET'])
def api_status_modelos():
    """Endpoint de diagnóstico para verificar el estado de los modelos"""
    status = {
        'ols': {
            'cargado': modelo_ols is not None,
            'trained': modelo_ols.trained if modelo_ols is not None else False,
            'variables': len(modelo_ols.variables) if modelo_ols is not None else 0
        },
        'bayesiano': {
            'cargado': modelo_bayes is not None,
            'trained': modelo_bayes.trained if modelo_bayes is not None else False,
            'variables': len(modelo_bayes.variables) if modelo_bayes is not None else 0
        }
    }
    return jsonify(status), 200


@app.route('/api/datos-ejemplo', methods=['GET'])
def api_datos_ejemplo():
    """Retorna datos de ejemplo para probar el formulario"""
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
        'calefaccion': 'hot air',
        'consumo_calefacion': 'gas',
        'desague': 'septic',
        'vistas_lago': 'No',
        'nueva_construccion': 'No',
        'aire_acondicionado': 'No'
    }
    return jsonify(ejemplo), 200


@app.route('/api/estadisticas', methods=['GET'])
def api_estadisticas():
    """Retorna estadísticas del dataset"""
    if not os.path.exists('data/SaratogaHouses.csv'):
        return jsonify({'error': 'Datos no disponibles'}), 404
    
    try:
        df = pd.read_csv('data/SaratogaHouses.csv')
        
        stats = {
            'total_casas': len(df),
            'precio_promedio': float(df['precio'].mean()),
            'precio_min': float(df['precio'].min()),
            'precio_max': float(df['precio'].max()),
            'precio_mediana': float(df['precio'].median()),
            'metros_promedio': float(df['metros_totales'].mean()),
            'antiguedad_promedio': float(df['antiguedad'].mean()),
            'dormitorios_promedio': float(df['dormitorios'].mean())
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/modelo-info', methods=['GET'])
def api_modelo_info():
    """Retorna información sobre los modelos entrenados"""
    try:
        info = {
            'modelos': {}
        }
        
        if modelo_ols is not None:
            info['modelos']['ols'] = {
                'tipo_modelo': 'Regresión Lineal Múltiple (OLS)',
                'metodologia': 'Frecuentista (Estadística Clásica)',
                'framework': 'statsmodels',
                'metricas': {
                    'r2': float(modelo_ols.modelo.rsquared),
                    'r2_ajustado': float(modelo_ols.modelo.rsquared_adj),
                    'rmse': float(np.sqrt(modelo_ols.modelo.mse_resid)),
                    'n_observaciones': int(modelo_ols.modelo.nobs),
                    'n_variables': len(modelo_ols.variables)
                },
                'variables': modelo_ols.variables
            }
        
        if modelo_bayes is not None:
            info['modelos']['bayesiano'] = {
                'tipo_modelo': 'Regresión Bayesiana',
                'metodologia': 'Bayesiana (Teorema de Bayes)',
                'framework': 'statsmodels (aproximación bayesiana)',
                'metricas': {
                    'r2': float(modelo_bayes.modelo.rsquared),
                    'r2_ajustado': float(modelo_bayes.modelo.rsquared_adj),
                    'rmse': float(np.sqrt(modelo_bayes.modelo.mse_resid)),
                    'n_observaciones': int(modelo_bayes.modelo.nobs),
                    'n_variables': len(modelo_bayes.variables)
                },
                'variables': modelo_bayes.variables,
                'prior': modelo_bayes.priors.get('tipo', 'No informativo')
            }
        
        if not info['modelos']:
            return jsonify({'error': 'Ningún modelo disponible'}), 404
        
        return jsonify(info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analisis-estadistico', methods=['GET'])
def api_analisis_estadistico():
    """
    API endpoint que retorna análisis estadístico completo con paso a paso
    Incluye: Normal, Binomial, Poisson, Esperanza, Bayes, Intervalos, Pruebas de Hipótesis
    
    Estos análisis se usan SOLO para fines académicos/estudio,
    NO interfieren con la predicción final del precio.
    """
    try:
        if not os.path.exists('data/SaratogaHouses.csv'):
            return jsonify({
                'error': 'Dataset no disponible. Ejecuta primero el análisis estadístico.'
            }), 404
        
        analizador = AnalisisEstadistico()
        analizador.cargar_datos()
        analisis_completo = analizador.generar_analisis_completo()
        
        # Convertir todos los valores NumPy a tipos nativos de Python
        analisis_completo = convertir_numpy_a_nativo(analisis_completo)
        
        return jsonify({
            'error': None,
            'analisis': analisis_completo,
            'nota': 'Estos análisis se realizan SOLO para fines académicos/estudio y NO interfieren con la predicción final del precio de las viviendas.'
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error al generar análisis: {str(e)}'
        }), 500


@app.route('/api/comparar', methods=['POST'])
def api_comparar():
    """
    Compara múltiples casas y retorna sus predicciones
    Útil para análisis comparativo
    """
    if modelo_ols is None and modelo_bayes is None:
        return jsonify({'error': 'Modelos no disponibles'}), 500
    
    try:
        lista_casas = request.get_json()
        
        if not isinstance(lista_casas, list):
            return jsonify({'error': 'Se esperaba una lista de casas'}), 400
        
        # Predecir cada casa individualmente con ambos modelos
        resultado = []
        for i, casa in enumerate(lista_casas):
            predicciones = {}
            
            if modelo_ols is not None:
                pred_ols = modelo_ols.predecir(casa)
                predicciones['ols'] = {
                    'precio_predicho': float(pred_ols['precio_estimado']),
                    'precio_formateado': f"${pred_ols['precio_estimado']:,.2f}",
                    'ic_inferior': float(pred_ols['ic_inferior_95']),
                    'ic_superior': float(pred_ols['ic_superior_95'])
                }
            
            if modelo_bayes is not None:
                pred_bayes = modelo_bayes.predecir(casa)
                predicciones['bayesiano'] = {
                    'precio_predicho': float(pred_bayes['precio_estimado']),
                    'precio_formateado': f"${pred_bayes['precio_estimado']:,.2f}",
                    'ic_inferior': float(pred_bayes['ic_inferior_95']),
                    'ic_superior': float(pred_bayes['ic_superior_95'])
                }
            
            resultado.append({
                'id': i + 1,
                'casa': casa,
                'predicciones': predicciones
            })
        
        return jsonify({
            'total': len(resultado),
            'predicciones': resultado
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Manejo de error 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejo de error 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" APLICACIÓN WEB DE PREDICCIÓN DE PRECIOS DE CASAS")
    print("=" * 60)
    
    if modelo_ols is None and modelo_bayes is None:
        print("\n  ⚠️  ADVERTENCIA: Ningún modelo encontrado")
        print("   Ejecuta primero: python3 analisis_estadistico.py")
        print("\n")
    else:
        print("\n Modelos cargados correctamente:")
        if modelo_ols is not None:
            print(f"   OLS (Frecuentista):    R² = {modelo_ols.modelo.rsquared:.4f} ({modelo_ols.modelo.rsquared*100:.2f}%)")
            print(f"                         RMSE = ${np.sqrt(modelo_ols.modelo.mse_resid):,.2f}")
        if modelo_bayes is not None:
            print(f"   Bayesiano:              R² = {modelo_bayes.modelo.rsquared:.4f} ({modelo_bayes.modelo.rsquared*100:.2f}%)")
            print(f"                         RMSE = ${np.sqrt(modelo_bayes.modelo.mse_resid):,.2f}")
        print("\n")
    
    print("Abriendo servidor en: http://127.0.0.1:5000")
    print("=" * 60)
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

