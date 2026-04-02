# Docker Hub Deployment - Support WiFi

## Images Disponibles sur Docker Hub

### Repository officiel
**URL**: https://hub.docker.com/r/mado87464/derangement-wifi

### Tags disponibles
- `mado87464/derangement-wifi:latest` - Version la plus récente
- `mado87464/derangement-wifi:v1.0.1` - Version stable 1.0.1

## Déploiement Rapide

### Option 1: Pull et Run
```bash
# Pull depuis Docker Hub
docker pull mado87464/derangement-wifi:latest

# Démarrer l'application
docker run -d -p 5000:5000 --name wifi-support-app mado87464/derangement-wifi:latest
```

### Option 2: Docker Compose
```bash
# Créer docker-compose.yml
version: '3.8'
services:
  wifi-support:
    image: mado87464/derangement-wifi:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=cle_secrete_production
    volumes:
      - ./data:/app/data
    restart: unless-stopped

# Démarrer
docker-compose up -d
```

### Option 3: Déploiement Production
```bash
# Pull version spécifique
docker pull mado87464/derangement-wifi:v1.0.1

# Démarrer avec configuration production
docker run -d \
  -p 5000:5000 \
  --name wifi-support-prod \
  --restart unless-stopped \
  -e FLASK_ENV=production \
  -e SECRET_KEY=votre_cle_secrete \
  -v /opt/wifi-support/data:/app/data \
  mado87464/derangement-wifi:v1.0.1
```

## Vérification du Déploiement

### Health Check
```bash
# Vérifier que l'application répond
curl http://localhost:5000

# Vérifier les logs
docker logs wifi-support-app
```

### Accès à l'Application
- **URL**: http://localhost:5000
- **Interface**: Support WiFi Dashboard
- **Fonctionnalités**: Inscription, Connexion, Gestion des tickets

## Informations sur l'Image

### Caractéristiques
- **Base Image**: Python 3.9-slim
- **Taille**: 232MB
- **Architecture**: linux/amd64
- **Exposé**: Port 5000

### Dépendances
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.3
- Flask-WTF 1.1.1
- Werkzeug 2.3.7

## Mises à Jour

### Mise à jour vers la dernière version
```bash
# Pull de la nouvelle version
docker pull mado87464/derangement-wifi:latest

# Redémarrer le container
docker stop wifi-support-app
docker rm wifi-support-app
docker run -d -p 5000:5000 --name wifi-support-app mado87464/derangement-wifi:latest
```

### Mise à jour avec Docker Compose
```bash
# Pull et redémarrage
docker-compose pull
docker-compose up -d
```

## Support

### Issues et Support
- **GitHub**: https://github.com/mado87464-sketch/DERANGEMENT_WIFI/issues
- **Docker Hub**: https://hub.docker.com/r/mado87464/derangement-wifi

### Documentation
- **Repository**: https://github.com/mado87464-sketch/DERANGEMENT_WIFI
- **README**: Documentation complète du projet

## Sécurité

### Variables d'Environnement
- `FLASK_ENV`: Mode d'exécution (production/development)
- `SECRET_KEY`: Clé secrète Flask (à personnaliser)

### Volumes Persistants
- `/app/data`: Données de la base de données SQLite

## Monitoring

### Logs
```bash
# Voir les logs en temps réel
docker logs -f wifi-support-app

# Voir les logs des 100 dernières lignes
docker logs --tail 100 wifi-support-app
```

### Statistiques
```bash
# Voir l'utilisation des ressources
docker stats wifi-support-app
```

## Backup

### Backup des données
```bash
# Backup de la base de données
docker exec wifi-support-app cp /app/wifi_support.db /app/data/backup_$(date +%Y%m%d).db
```

### Restore
```bash
# Restore depuis un backup
docker exec wifi-support-app cp /app/data/backup_YYYYMMDD.db /app/wifi_support.db
```

---

**L'application Support WiFi est maintenant disponible sur Docker Hub !** 🐳
