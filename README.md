# Inventaire des harnesses et agents IA

Jeu de données consolidé au **2026-08-29** : **173** systèmes (harnesses de codage, IDE agentiques, agents cloud, orchestrateurs, frameworks et agents de recherche).

Le fichier principal est [`inventaire.csv`](inventaire.csv). Il regroupe la fiche de chaque outil, le type de source et la définition taxonomique de sa catégorie.

> Les cellules `Inconnu / non documenté` signalent une information non confirmée. Elles ne signifient pas que la fonction est absente. Vérifiez la source principale avant un achat ou un déploiement.

## Fichiers

| Fichier | Contenu |
|---|---|
| [`inventaire.csv`](inventaire.csv) | Table unique, 173 lignes × 31 colonnes |
| [`taxonomie.csv`](taxonomie.csv) | Définitions des catégories |
| [`sources.csv`](sources.csv) | 133 URL utilisées, avec type (primaire / secondaire) |
| [`dictionnaire.csv`](dictionnaire.csv) | Dictionnaire des champs et de la légende |

Encodage : **UTF-8**, séparateur `,`, dates **ISO 8601** (`YYYY-MM-DD`), fin de ligne LF.

## Colonnes de `inventaire.csv`

| Colonne | Rôle |
|---|---|
| `id` | Identifiant stable (slug ASCII) |
| `nom` | Nom du système |
| `editeur` | Éditeur ou mainteneur |
| `categorie` | Catégorie de l’inventaire |
| `acces` | Open source, hybride, propriétaire… |
| `licence` | Licence ou conditions documentées |
| `maturite` | Actif, expérimental, archivé… |
| `surfaces` | CLI, IDE, web, cloud… |
| `local` / `cloud` | Où ça s’exécute |
| `politique_modeles` | Modèles supportés |
| `terminal` `ide` `web` `computer_use` | Surfaces d’interaction |
| `mcp` `acp` `skills` `sous_agents` | Protocoles et composition |
| `memoire` `sandbox` `orchestration` | Mémoire, isolation, coordination |
| `usage_principal` | Usage observé |
| `source_principale` | URL de référence |
| `type_source` | Primaire / dépôt ou secondaire / index |
| `notes` | Remarque ponctuelle |
| `confiance` | Élevée, moyenne ou faible |
| `verifie_le` | Date de vérification |
| `definition_categorie` `est_harness` `remarque_categorie` | Jointure depuis `taxonomie.csv` |

## Répartition

**Catégories**

| Catégorie | n |
|---|---|
| Coding harness | 42 |
| Framework / SDK | 26 |
| Orchestrator | 24 |
| Research coding agent | 22 |
| Meta-harness / workspace | 11 |
| Agentic IDE | 10 |
| General-purpose agent | 10 |
| Cloud coding agent | 8 |
| App-building agent | 7 |
| Coding agent | 4 |
| Agent runtime | 3 |
| Autonomous loop | 2 |
| Agent platform | 1 |
| Agent bridge | 1 |
| Review / coding agent | 1 |
| Review agent | 1 |

**Accès** : 76 open source · 52 propriétaires · 22 open source / recherche · 16 open source / hybride · 7 autres.

**Confiance** : 78 élevée · 83 moyenne · 12 faible.

## Périmètre

Inclus : harnesses de codage, agents généralistes capables de coder, plateformes d’agents, orchestrateurs et frameworks adjacents.

Exclus : modèles seuls, simples autocomplétions sans boucle agentique, petits forks non identifiés et wrappers éphémères.

Méthode : documentations et dépôts officiels en priorité ; listes communautaires pour le long tail. Les licences et fonctionnalités doivent être revérifiées avant un usage juridique.

## Utilisation

```bash
# aperçu
head -n 2 inventaire.csv

# Python
python3 -c "import csv; rows=list(csv.DictReader(open('inventaire.csv', encoding='utf-8'))); print(len(rows), rows[0]['nom'])"
```

Les licences listées sont celles des projets inventoriés, pas une licence de ce jeu de données. Ajoutez la vôtre avant publication publique si besoin.
