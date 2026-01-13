# Forum Anonyme

Projet de forum anonyme avec architecture microservices, Docker Swarm et CI/CD automatisée.

## Architecture

- **Front** : Interface web Flask (port 80)
- **API** : API REST Flask (port 5000)
- **DB** : PostgreSQL (interne au backend)

## Stack technique

- **Backend** : Python 3.9, Flask, PostgreSQL
- **Infrastructure** : Docker, Docker Swarm
- **CI/CD** : GitHub Actions (validation, tests, build, deploy)
- **Qualité** : Black, Flake8, Mypy, Pytest
- **Registry** : GitHub Container Registry (GHCR)

## Convention de commits (Conventional Commits)

Format requis : **`type(scope): message`**

Types autorisés : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

### Commitizen

- **Installer (global, comme demandé)** :
  - `npm install -g commitizen cz-conventional-changelog`
- **Ou recommandé (local au projet)** :
  - `npm install`

Puis faire un commit avec l’assistant :

- `npm run commit`

### Vérification automatique du format (commitlint + husky)

Après installation des dépendances, activer les hooks :

- `npm run prepare`

Note : le **scope est obligatoire** (ex: `feat(tooling): ajoute commitizen`), sinon le commit est refusé par commitlint.

## Versioning automatique (bonus)

Le projet est configuré pour utiliser **standard-version** afin de générer automatiquement :

- la version (basée sur les commits)
- `CHANGELOG.md`
- les tags Git

Commandes :

- `npm run release` (auto)
- `npm run release:patch` / `npm run release:minor` / `npm run release:major`

## Développement local

### Prérequis

- Python 3.9+
- Docker & Docker Compose
- Node.js (pour commitizen/versioning)

### Installation

```bash
# Dépendances Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt -r api/requirements-dev.txt
pip install -r front/requirements.txt -r front/requirements-dev.txt

# Dépendances Node (optionnel)
npm install
```

### Lancer le projet

```bash
docker compose up --build
```

Accès : `http://localhost` (ou `http://localhost:8080` si port 80 occupé)

### Tests & Qualité

```bash
# Formatage
black .

# Linting
flake8

# Type checking
mypy api front

# Tests unitaires
pytest -m "not integration and not e2e"

# Tests complets (avec DB + E2E)
docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d
DB_HOST=localhost pytest -m integration
E2E_BASE_URL=http://localhost:8080 pytest -m e2e
docker compose down
```

## Déploiement

### Prérequis VPS

1. Docker installé
2. Swarm initialisé :

```bash
# Sur le manager
./swarm/setup-manager.sh <VPS_IP>

# Sur le worker (optionnel)
./swarm/setup-worker.sh <TOKEN> <MANAGER_IP>
```

3. Secret Swarm créé :

```bash
printf 'password' | docker secret create forum_db_password -
```

### Déploiement manuel

```bash
export REPO="<owner>/<repo>"
export IMAGE_TAG="<sha7>"
docker stack deploy -c docker-stack.yml forum-anonyme --with-registry-auth
```

### Déploiement automatique (CI/CD)

Le déploiement est automatique sur push vers `main`/`master` via GitHub Actions.

Voir [CI_CD_GUIDE.md](./CI_CD_GUIDE.md) pour plus de détails.

## Structure du projet

```
forum-anonyme/
├── api/                    # API REST
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
├── front/                  # Interface web
│   ├── app.py
│   ├── templates/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
├── db/                     # Base de données
│   ├── Dockerfile
│   └── init.sql
├── swarm/                  # Scripts Swarm
│   ├── setup-manager.sh
│   └── setup-worker.sh
├── .github/workflows/      # CI/CD
│   └── cicd.yml
├── docker-compose.yml      # Dev local
├── docker-compose.ci.yml   # CI override
├── docker-stack.yml        # Production Swarm
└── CI_CD_GUIDE.md          # Guide CI/CD
```
