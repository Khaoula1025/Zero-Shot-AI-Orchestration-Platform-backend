# Hybrid-Analyzer Backend

## 📋 Vue d'ensemble

Backend de l'application Hybrid-Analyzer - Une API REST Python qui orchestre deux services d'intelligence artificielle (Hugging Face et Gemini) pour automatiser l'analyse et la classification d'articles de presse.

## 🎯 Fonctionnalités principales

- **Authentification sécurisée** : Système JWT avec registration et login
- **Orchestration IA** : Chaînage automatique Hugging Face → Gemini
- **Classification Zero-Shot** : Catégorisation de textes via facebook/bart-large-mnli
- **Analyse contextuelle** : Synthèse et détection de ton via Gemini API
- **Gestion robuste des erreurs** : Timeouts, retries, logs détaillés
- **Base de données PostgreSQL** : Stockage sécurisé des utilisateurs


## 🚀 Technologies

- **Python 3.11+**
- **FastAPI** - Framework web asynchrone
- **SQLAlchemy** - ORM PostgreSQL
- **Alembic** - Migrations de base de données
- **bcrypt** - Hachage sécurisé des mots de passe
- **PyJWT** - Gestion des tokens JWT
- **httpx** - Client HTTP asynchrone
- **pytest** - Tests unitaires
- **Docker & Docker Compose** - Containerisation

## 📦 Structure du projet

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                        # Point d'entrée FastAPI
│   ├── dependencies.py                # Dépendances injectables
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logger.py                  # Configuration logging
│   │   └──  security.py               # JWT & bcrypt   
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                    # Modèles SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                    # Schémas authentification
│   │   └── articles.py                # Schémas analyse
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_services_filter.py    # Logique authentification
│   │   ├── huggingface.py             # Client Hugging Face
│   │   └── gemini_api.py              # Client Gemini
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── authRouter.py              # Routes /register, /login
│   │   └── analyzeRouter.py           # Route /analyze
│   └── db/
│       └── database.py                # Connexion PostgreSQL
├── tests/
│   ├── __init__.py
│   ├── test_complet.py
│   ├── test_hugging_face.py
│   └── test_gemini.py
├── .env                               # Variables d'environnement
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## ⚙️ Installation et Configuration

### Prérequis

- Python 3.11+
- PostgreSQL 15+ (ou Docker)
- Clés API :
  - [Hugging Face API Token](https://huggingface.co/settings/tokens)
  - [Google Gemini API Key](https://makersuite.google.com/app/apikey)


### Installation avec Docker (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/Khaoula1025/Zero-Shot-AI-Orchestration-Platform-backend.git

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Lancer avec Docker Compose
docker-compose up -d


# L'API sera accessible sur http://localhost:8000
# Documentation interactive : http://localhost:8000/docs
```

### Installation manuelle

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur de développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

### Endpoints

#### 1. Authentification

**POST /register**

Créer un nouveau compte utilisateur.

```json
// Request
{
  "username": "john_doe",
  "password": "SecurePass123!"
}

// Response 201
{
  "message": "User created successfully",
  "user_id": 1,
  "username": "john_doe"
}
```

**POST /login**

Authentifier un utilisateur et obtenir un token JWT.

```json
// Request
{
  "username": "john_doe",
  "password": "SecurePass123!"
}

// Response 200
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### 2. Analyse (Protégé par JWT)

**POST /analyze**

Analyser un texte via Hugging Face et Gemini.

```bash
# Headers requis
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

```json
// Request
{
  "text": "Apple Inc. annonce des résultats trimestriels exceptionnels avec une croissance de 15% du chiffre d'affaires, portée par les ventes d'iPhone et les services cloud."
}

// Response 200
{
  "category": "Finance",
  "confidence_score": 0.89,
  "summary": "Apple rapporte une forte croissance trimestrielle de 15%, principalement grâce aux iPhone et services cloud.",
  "tone": "positive",
  "processing_time": 3.24,
  "timestamp": "2025-12-12T10:30:45.123Z"
}
```

### Documentation interactive

Une fois le serveur lancé :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔄 Workflow d'analyse

```
1. Client → POST /analyze + JWT token
              ↓
2. Backend valide le token JWT
              ↓
3. Appel Hugging Face (facebook/bart-large-mnli)
   - Catégories : Finance, RH, IT, Opérations, etc.
   - Retour : Catégorie + Score de confiance
              ↓
4. Construction du prompt contextualisé pour Gemini
   - Inclusion de la catégorie prédite
   - Demande de synthèse + analyse de ton
              ↓
5. Appel Gemini API
   - Génération du résumé
   - Détection du ton (positif/négatif/neutre)
              ↓
6. Agrégation des résultats
              ↓
7. Retour JSON structuré au client
```

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest

# Avec couverture de code
pytest --cov=app --cov-report=html

# Tests spécifiques
pytest tests/test_auth.py -v
pytest tests/test_analysis.py -v

# Tests avec logs détaillés
pytest -s -v
```

## 🔒 Sécurité

### Mesures implémentées

- **Hachage bcrypt** : Mots de passe hashés avec salt (cost factor: 12)
- **JWT signé** : Tokens avec expiration configurable
- **Validation Pydantic** : Toutes les entrées sont validées
- **Secrets externalisés** : Clés API dans variables d'environnement

## 📊 Logging

### Configuration

Le système de logging est centralisé dans `app/core/logger.py` :

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)

logger = logging.getLogger("app")
```

### Niveaux de logs

- **INFO** : Opérations normales (analyse démarrée, utilisateur connecté)
- **WARNING** : Situations inhabituelles (score faible, timeout)
- **ERROR** : Erreurs récupérables (API down, réponse invalide)
- **CRITICAL** : Erreurs critiques (DB inaccessible, clé API manquante)

### Exemple de logs

```
2025-12-12 10:30:15 - app.auth - INFO - User 'john_doe' logged in successfully
2025-12-12 10:31:02 - app.analysis - INFO - Starting analysis for text (247 chars)
2025-12-12 10:31:03 - app.huggingface - INFO - Classification result: Finance (0.87)
2025-12-12 10:31:05 - app.gemini - INFO - Synthesis completed successfully
2025-12-12 10:31:05 - app.analysis - INFO - Analysis completed in 3.2s
```

## ⚠️ Gestion des erreurs

### Stratégies par service

#### Hugging Face
- **Timeout (>30s)** : Retry automatique (max 3 tentatives avec backoff)
- **Score faible (<0.5)** : Warning dans les logs + flag dans la réponse
- **API indisponible** : Erreur 503 avec message explicite
- **Rate limit** : Attente + retry exponentiel

#### Gemini
- **Réponse mal formée** : Parsing robuste avec fallback
- **Rate limit** : Queue de retry avec exponential backoff
- **Contenu filtré** : Message d'erreur approprié
- **Token limit dépassé** : Troncature du texte

#### Base de données
- **Connexion perdue** : Pool de connexions avec reconnexion auto
- **Contrainte unique violée** : Message d'erreur explicite
- **Transaction échouée** : Rollback automatique + log

## 🚧 Limites et considérations

### Dépendances externes

- **Hugging Face** :
  - Latence : 1-5 secondes par requête
  - Rate limit : 30 000 requêtes/mois (plan gratuit)
  - Disponibilité : ~99.5% (selon status.huggingface.co)

- **Gemini API** :
  - Latence : 2-8 secondes selon la taille du texte
  - Coût : Facturation par token (voir pricing Google)
  - Rate limit : Selon le plan choisi

### Optimisations recommandées

1. **Cache Redis** : Stocker les analyses récentes
2. **Queue asynchrone** : Celery pour les analyses longues
3. **Batch processing** : Traiter plusieurs textes en parallèle
4. **Prompt engineering** : Optimiser les prompts Gemini pour réduire les tokens

## 🐳 Docker

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: hybrid_analyzer
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/hybrid_analyzer
    depends_on:
      - postgres
    volumes:
      - ./app:/app/app
      - ./logs:/app/logs

volumes:
  postgres_data:
```

### Commandes Docker utiles

```bash
# Build et démarrage
docker-compose up --build -d

# Voir les logs
docker-compose logs -f backend

# Arrêt
docker-compose down

# Nettoyage complet
docker-compose down -v
```
## 📝 Prochaines étapes

- [ ] Ajouter un système de cache (Redis)
- [ ] Implémenter rate limiting par utilisateur
- [ ] Ajouter monitoring (Prometheus + Grafana)
- [ ] Créer des endpoints d'administration
- [ ] Implémenter l'historique des analyses
- [ ] Ajouter support multi-langue


## 📞 Support

- **Issues** : [GitHub Issues](your-repo-url/issues)
- **Documentation** : http://localhost:8000/docs
- **Contact** : khaoula.esioudi@gmail.com

---

**Version** : 1.0.0  
**Date de livraison** : 12 décembre 2025  