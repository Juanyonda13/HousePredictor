from app import create_app

app = create_app()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" APLICACIÓN WEB DE PREDICCIÓN DE PRECIOS DE CASAS")
    print("=" * 60)

    if not app.extensions["model_service"].has_any_model():
        print("\n  ⚠️  ADVERTENCIA: Ningún modelo encontrado")
        print("   Ejecuta primero: python3 analisis_estadistico.py\n")
    else:
        print("\n Modelos cargados correctamente ✅\n")

    print("Abriendo servidor en: http://127.0.0.1:5000")
    print("=" * 60)
    print("\nPresiona Ctrl+C para detener el servidor\n")

    app.run(debug=True, host="0.0.0.0", port=5000)
