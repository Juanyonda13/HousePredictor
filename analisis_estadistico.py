#!/usr/bin/env python3
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

from model.regresion_lineal import ModeloRegresionLineal
from model.regresion_bayesiana import ModeloRegresionBayesiana

warnings.filterwarnings("ignore")

DATA_PATH = Path("data/SaratogaHouses.csv")


def cargar_datos() -> pd.DataFrame:
    """Carga el dataset requerido por los modelos."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {DATA_PATH}. Descarga el dataset o ejecuta model/train.py."
        )

    df = pd.read_csv(DATA_PATH)

    print("\n" + "=" * 80)
    print("DATOS CARGADOS")
    print("=" * 80)
    print(f"Total de observaciones: {len(df)}")
    print(f"Columnas: {', '.join(df.columns.tolist())}")
    print("Estadísticas básicas del precio:")
    print(df["precio"].describe())

    return df


def entrenar_modelo_ols(df: pd.DataFrame) -> dict:
    """Entrena y guarda el modelo de Regresión Lineal (Frecuentista)."""
    print("\n" + "=" * 80)
    print("ENTRENANDO MODELO FRECUENTISTA (OLS)")
    print("=" * 80)

    modelo_ols = ModeloRegresionLineal()
    metricas_ols = modelo_ols.entrenar(df)
    modelo_ols.guardar()

    print("\n✅ Modelo OLS guardado en model/modelo_regresion_lineal.pkl")
    print("   Variables utilizadas:", ", ".join(modelo_ols.variables))
    print(
        f"   R²: {metricas_ols['r2']:.4f} "
        f"({metricas_ols['r2'] * 100:.2f}%) | "
        f"RMSE: ${metricas_ols['rmse']:,.2f}"
    )

    return metricas_ols


def entrenar_modelo_bayesiano(df: pd.DataFrame) -> dict:
    """Entrena y guarda el modelo Bayesiano."""
    print("\n" + "=" * 80)
    print("ENTRENANDO MODELO BAYESIANO")
    print("=" * 80)

    modelo_bayes = ModeloRegresionBayesiana()
    metricas_bayes = modelo_bayes.entrenar(df)
    modelo_bayes.guardar()

    print("\n✅ Modelo Bayesiano guardado en model/modelo_regresion_bayesiana.pkl")
    print(
        f"   R²: {metricas_bayes['r2']:.4f} "
        f"({metricas_bayes['r2'] * 100:.2f}%) | "
        f"RMSE: ${metricas_bayes['rmse']:,.2f}"
    )

    return metricas_bayes


def main() -> None:
    print("=" * 80)
    print("PIPELINE DE ENTRENAMIENTO PARA LA APLICACIÓN WEB")
    print("=" * 80)

    df = cargar_datos()

    metricas_ols = entrenar_modelo_ols(df)
    metricas_bayes = entrenar_modelo_bayesiano(df)

    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    print(
        f"OLS:     R² = {metricas_ols['r2']:.4f} "
        f"({metricas_ols['r2'] * 100:.2f}%), "
        f"RMSE = ${metricas_ols['rmse']:,.2f}"
    )
    print(
        f"Bayes:   R² = {metricas_bayes['r2']:.4f} "
        f"({metricas_bayes['r2'] * 100:.2f}%), "
        f"RMSE = ${metricas_bayes['rmse']:,.2f}"
    )
    print("\nModelos listos para ser usados por app.py ✅")


if __name__ == "__main__":
    main()

