# Forum Anonyme

Projet de forum anonyme utilisant Docker et Docker Compose.

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
