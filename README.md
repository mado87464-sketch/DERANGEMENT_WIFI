# Support WiFi - Application de Gestion de Tickets

## Description
Application Flask pour la gestion des pannes de connexion WiFi permettant aux clients de signaler des problèmes et aux agents de les gérer.

## Démarrage Rapide

### Option 1: Docker (Recommandé)
```bash
# Clonez le repository
git clone https://github.com/mado87464-sketch/DERANGEMENT_WIFI.git
cd DERANGEMENT_WIFI

# Démarrage avec Docker Compose
docker-compose up -d
```

L'application sera accessible sur http://localhost:5000

### Option 2: Installation Locale
```bash
# Clonez le repository
git clone https://github.com/mado87464-sketch/DERANGEMENT_WIFI.git
cd DERANGEMENT_WIFI

# Installation des dépendances
pip install -r requirements.txt

# Démarrage
python app.py
```

## Fonctionnalités

### Client
- Inscription et connexion sécurisées
- Création de tickets de support
- Suivi des tickets créés
- Communication avec les agents

### Agent
- Inscription et connexion sécurisées
- Vue de tous les tickets
- Gestion des statuts des tickets
- Communication avec les clients

## Technologies

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, Font Awesome
- **Base de données**: SQLite
- **Containerisation**: Docker, Docker Compose
- **Déploiement**: Docker Hub

## CI/CD Pipeline

### GitHub Actions
Le projet utilise GitHub Actions pour l'intégration continue et le déploiement automatique :

1. **CI Tests** (`ci.yml`) : Tests automatiques à chaque push/PR
2. **Docker Build** (`docker.yml`) : Build et push vers Docker Hub
3. **Déploiement** (`deploy.yml`) : Déploiement automatique en production

### Configuration GitHub Secrets
Configurez ces secrets dans votre repository GitHub :

```
DOCKER_USERNAME=mado87464
DOCKER_PASSWORD=votre_docker_hub_token
PROD_HOST=votre_serveur_ip
PROD_USER=votre_utilisateur_ssh
PROD_SSH_KEY=votre_cle_ssh_privee
PROD_URL=https://votre-domaine.com
```

### Workflow Automatique
1. **Push sur main** → Tests → Build Docker → Push Docker Hub
2. **Release** → Déploiement automatique en production
3. **Pull Request** → Tests complets

## Déploiement avec Docker Hub

```bash
# Pull depuis Docker Hub
docker pull mado87464/derangement-wifi:latest

# Démarrage
docker run -p 5000:5000 mado87464/derangement-wifi:latest
```

## Structure du Projet

```
DERANGEMENT_WIFI/
├── app.py                 # Application principale
├── requirements.txt        # Dépendances Python
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Configuration Docker Compose
├── .dockerignore        # Fichiers ignorés par Docker
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── client_dashboard.html
│   ├── agent_dashboard.html
│   ├── create_ticket.html
│   └── view_ticket.html
└── data/               # Données persistantes
```

## Auteur

Projet réalisé pour la gestion des pannes de connexion WiFi.
