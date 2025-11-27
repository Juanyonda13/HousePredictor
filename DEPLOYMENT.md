# Guia de Despliegue - Prediccion de Casas ML

## Arquitectura

- **Docker**: Contenedor Flask
- **Nginx Proxy Manager**: Reverse proxy + SSL
- **Red webproxy**: Red compartida
- **Puerto**: 5000

## Despliegue Inicial

```bash
# 1. Entrenar modelo (local)
python3 analisis_estadistico.py

# 2. Desplegar al servidor
./deploy-to-hostinger.sh

# 3. Configurar dominio en NPM (http://168.231.71.181:8080)
#    - Domain: prediccion-casas.tu-dominio.com
#    - Forward: prediccion-casas-web:5000
#    - SSL: Let's Encrypt
```

## Actualizacion Rapida

```bash
./update-deployment.sh
```

## Comandos Utiles

```bash
# Ver logs
ssh hostinger 'docker logs -f prediccion-casas-web'

# Estado
ssh hostinger 'docker ps | grep prediccion-casas'

# Reiniciar
ssh hostinger 'cd /root/projects/prediccion-casas-ml && docker compose restart'
```

## Acceso

- Directo: http://168.231.71.181:5000
- Con dominio: https://prediccion-casas.tu-dominio.com
