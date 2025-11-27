"""
Script para entrenar el modelo de prediccion de precios de casas
Basado en el notebook de Perceptron Multiple
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import multiprocessing
import warnings
warnings.filterwarnings('ignore')


def cargar_datos():
    """Carga los datos desde GitHub"""
    print(" Cargando datos...")
    url = ("https://raw.githubusercontent.com/JoaquinAmatRodrigo/"
           "Estadistica-machine-learning-python/master/data/SaratogaHouses.csv")
    
    datos = pd.read_csv(url, sep=",")
    
    datos.columns = ["precio", "metros_totales", "antiguedad", "precio_terreno",
                     "metros_habitables", "universitarios", "dormitorios", 
                     "chimenea", "banyos", "habitaciones", "calefaccion",
                     "consumo_calefacion", "desague", "vistas_lago",
                     "nueva_construccion", "aire_acondicionado"]
    
    print(f"? Datos cargados: {datos.shape[0]} casas con {datos.shape[1]} caracteristicas")
    return datos


def preparar_datos(datos):
    """Divide los datos en entrenamiento y prueba"""
    print("\n Dividiendo datos en entrenamiento y prueba...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        datos.drop('precio', axis=1),
        datos['precio'],
        train_size=0.8,
        random_state=142,
        shuffle=True
    )
    
    print(f"   Entrenamiento: {X_train.shape[0]} casas")
    print(f"   Prueba: {X_test.shape[0]} casas")
    
    return X_train, X_test, y_train, y_test


def crear_preprocessor(X_train):
    """Crea el pipeline de preprocesamiento"""
    print("\n Creando pipeline de preprocesamiento...")
    
    # Identificar columnas numericas y categoricas
    numeric_cols = X_train.select_dtypes(include=['float64', 'int']).columns.to_list()
    cat_cols = X_train.select_dtypes(include=['object', 'category']).columns.to_list()
    
    print(f"   Variables numericas: {len(numeric_cols)}")
    print(f"   Variables categoricas: {len(cat_cols)}")
    
    # Transformaciones para las variables numericas
    numeric_transformer = Pipeline(
        steps=[('scaler', StandardScaler())]
    )
    
    # Transformaciones para las variables categoricas
    categorical_transformer = Pipeline(
        steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))]
    )
    
    # Combinar transformaciones
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, cat_cols)
        ],
        remainder='passthrough'
    )
    
    return preprocessor, numeric_cols, cat_cols


def entrenar_modelo(X_train_prep, y_train):
    """Entrena el modelo con busqueda de hiperparametros"""
    print("\n Entrenando modelo de Red Neuronal...")
    print("   (Esto puede tomar varios minutos...)")
    
    modelo = MLPRegressor(activation='relu', max_iter=2000, random_state=142)
    
    # Definir el espacio de busqueda de hiperparametros
    param_distributions = {
        'hidden_layer_sizes': [(10,), (20,), (10, 10), (20, 10)],
        'alpha': np.logspace(-3, 3, 10),
        'learning_rate_init': [0.001, 0.01],
    }
    
    # Busqueda aleatoria con validacion cruzada
    grid = RandomizedSearchCV(
        estimator=modelo,
        param_distributions=param_distributions,
        n_iter=30,  # Reducido para ser mas rapido
        scoring='neg_mean_squared_error',
        n_jobs=multiprocessing.cpu_count() - 1,
        cv=3,
        verbose=1,
        random_state=123,
        return_train_score=True
    )
    
    grid.fit(X=X_train_prep, y=y_train)
    
    modelo_final = grid.best_estimator_
    
    print("\n? Modelo entrenado exitosamente!")
    print(f"   Mejores parametros: {grid.best_params_}")
    
    return modelo_final, grid


def evaluar_modelo(modelo, X_test_prep, y_test):
    """Evalua el modelo en el conjunto de prueba"""
    print("\n Evaluando modelo en conjunto de prueba...")
    
    predicciones = modelo.predict(X=X_test_prep)
    
    # Calcular metricas
    mse = mean_squared_error(y_true=y_test, y_pred=predicciones)
    rmse = np.sqrt(mse)  # Calcular RMSE manualmente
    r2 = r2_score(y_true=y_test, y_pred=predicciones)
    
    print(f"\n Resultados:")
    print(f"   RMSE (Error promedio): ${rmse:,.2f}")
    print(f"   R2 Score: {r2:.4f}")
    print(f"   Precio promedio real: ${y_test.mean():,.2f}")
    
    return rmse, r2, predicciones


def guardar_modelo(modelo, preprocessor, numeric_cols, cat_cols):
    """Guarda el modelo y preprocesador entrenados"""
    print("\n Guardando modelo...")
    
    # Guardar modelo
    joblib.dump(modelo, 'model/modelo_casas.pkl')
    print("   ? Modelo guardado: model/modelo_casas.pkl")
    
    # Guardar preprocesador
    joblib.dump(preprocessor, 'model/preprocessor.pkl')
    print("   ? Preprocesador guardado: model/preprocessor.pkl")
    
    # Guardar nombres de columnas
    joblib.dump({
        'numeric_cols': numeric_cols,
        'cat_cols': cat_cols
    }, 'model/columns.pkl')
    print("   ? Columnas guardadas: model/columns.pkl")


def main():
    """Funcion principal de entrenamiento"""
    print("=" * 60)
    print(" ENTRENAMIENTO DEL MODELO DE PREDICCION DE PRECIOS DE CASAS")
    print("=" * 60)
    
    # 1. Cargar datos
    datos = cargar_datos()
    
    # Guardar una copia de los datos
    datos.to_csv('data/SaratogaHouses.csv', index=False)
    print("   ? Datos guardados en data/SaratogaHouses.csv")
    
    # 2. Preparar datos
    X_train, X_test, y_train, y_test = preparar_datos(datos)
    
    # 3. Crear preprocesador
    preprocessor, numeric_cols, cat_cols = crear_preprocessor(X_train)
    
    # 4. Aplicar preprocesamiento
    print("\n Aplicando transformaciones...")
    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)
    print("   ? Datos preprocesados")
    
    # 5. Entrenar modelo
    modelo_final, grid = entrenar_modelo(X_train_prep, y_train)
    
    # 6. Evaluar modelo
    rmse, r2, predicciones = evaluar_modelo(modelo_final, X_test_prep, y_test)
    
    # 7. Guardar modelo
    guardar_modelo(modelo_final, preprocessor, numeric_cols, cat_cols)
    
    print("\n" + "=" * 60)
    print(" !ENTRENAMIENTO COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print("\nEl modelo esta listo para ser usado en la aplicacion web.")
    print("Ejecuta: python app.py")


if __name__ == "__main__":
    main()

