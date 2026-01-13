# Guide CI/CD - Forum Anonyme

## Vue d'ensemble du Pipeline

Le workflow CI/CD se compose de 4 jobs séquentiels :

1. **Validation** (lint/format/typecheck)
2. **Tests** (unitaires + intégration + e2e)
3. **Build** (images Docker → GHCR)
4. **Deploy** (Docker Swarm via SSH)

## Job 1 : Validation

### Ce qui est vérifié
- **Black** : formatage du code (line-length 88, double quotes)
- **Flake8** : erreurs de style Python
- **Mypy** : type checking

### En cas d'échec

#### Black échoue
```bash
# Reformater localement
black .
git add .
git commit -m "style(format): applique black"
git push
```

#### Flake8 échoue
Erreurs courantes :
- Lignes trop longues (max 88) → couper ou reformater
- Imports inutilisés → supprimer
- Variables non utilisées → préfixer par `_`

#### Mypy échoue
- Ajouter des annotations de type si nécessaire
- Utiliser `# type: ignore` en dernier recours
- Config actuelle : `ignore_missing_imports = true`

## Job 2 : Tests

### Tests unitaires
Lancés automatiquement (sans DB/browser).

En cas d'échec :
```bash
pytest -m "not integration and not e2e" -v
```

### Tests d'intégration
Nécessitent une DB PostgreSQL (lancée via Docker Compose en CI).

En cas d'échec :
- Vérifier que la DB démarre (`docker compose logs db`)
- Vérifier les healthchecks
- Vérifier les variables d'environnement (`DB_HOST`, etc.)

### Tests E2E
Nécessitent Playwright + le stack complet.

En cas d'échec :
- Vérifier que le front est accessible (`curl http://localhost:8080`)
- Vérifier les logs du front/api
- Augmenter les timeouts si nécessaire

## Job 3 : Build

### Ce qui est fait
- Build des images Docker pour `api`, `front`, `db`
- Tag avec le hash court du commit (`<sha7>`)
- Push vers GitHub Container Registry (GHCR)

### En cas d'échec

#### Login GHCR échoue
- Vérifier que le secret `GHCR_TOKEN` est configuré
- Vérifier que le token a les permissions `write:packages`

#### Build Docker échoue
- Vérifier les Dockerfiles
- Tester localement :
  ```bash
  docker build -t test ./api
  docker build -t test ./front
  docker build -t test ./db
  ```

## Job 4 : Deploy

### Ce qui est fait
- Connexion SSH au VPS manager
- Login GHCR sur le VPS
- Création du secret Swarm `forum_db_password` (si absent)
- Déploiement du stack : `docker stack deploy -c docker-stack.yml forum-anonyme`

### En cas d'échec

#### SSH échoue
- Vérifier les secrets : `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`
- Tester manuellement : `ssh -i <key> user@host`

#### Login GHCR sur VPS échoue
- Vérifier que le token `GHCR_TOKEN` est valide
- Tester sur le VPS : `echo $TOKEN | docker login ghcr.io -u <user> --password-stdin`

#### Stack deploy échoue
- Vérifier que Swarm est initialisé : `docker node ls`
- Vérifier les logs : `docker stack ps forum-anonyme`
- Vérifier le secret : `docker secret ls`

## Secrets GitHub à configurer

Dans **Settings → Secrets and variables → Actions** :

| Secret | Description | Exemple |
|--------|-------------|---------|
| `GHCR_TOKEN` | Token GitHub pour push/pull images | `ghp_...` |
| `VPS_HOST` | IP du VPS manager | `31.207.36.148` |
| `VPS_USER` | User SSH | `root` |
| `VPS_SSH_KEY` | Clé privée SSH (format PEM) | `-----BEGIN OPENSSH...` |

## Tests locaux avant push

```bash
# 1. Qualité du code
black --check .
flake8
mypy api front

# 2. Tests
pytest

# 3. Build Docker
docker compose build

# 4. Test du stack
docker compose up -d
curl http://localhost
docker compose down
```

## Dépannage rapide

### Le workflow ne se déclenche pas
- Vérifier que le fichier `.github/workflows/cicd.yml` existe
- Vérifier les branches configurées (`main` / `master`)

### Le job Build ne se lance pas
- Build ne se lance que sur `push` (pas sur PR)

### Le job Deploy ne se lance pas
- Deploy ne se lance que sur `push` vers `main`/`master`
- Vérifier que Build a réussi (Deploy dépend de Build)

### Les tests d'intégration/e2e sont skippés en local
C'est normal. Pour les lancer :
```bash
# Intégration DB
docker compose up -d db
DB_HOST=localhost DB_NAME=forum DB_USER=postgres DB_PASSWORD=password pytest -m integration

# E2E
pip install playwright
playwright install
docker compose up -d
E2E_BASE_URL=http://localhost pytest -m e2e
docker compose down
```
