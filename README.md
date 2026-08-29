# AI harness and agent inventory

Dataset as of **2026-08-29**: **183** systems (coding harnesses, agentic IDEs, cloud coding agents, orchestrators, frameworks, research coding agents, and science agents).

The main file is [`inventaire.csv`](inventaire.csv). Each row is one tool, with its source type and category definition. You can also browse the table in [Airtable](https://airtable.com/appiub9AiVcxpuXAz/shrfiLQMtERFkwZN5).

> Cells marked `Inconnu / non documenté` mean the fact was not confirmed. They do not mean the feature is missing. Check the primary source before buying or deploying.

## Files

| File | Contents |
|---|---|
| [`inventaire.csv`](inventaire.csv) | Main table, 183 rows × 33 columns |
| [`taxonomie.csv`](taxonomie.csv) | Category definitions |
| [`sources.csv`](sources.csv) | 152 URLs, with primary / secondary type |
| [`dictionnaire.csv`](dictionnaire.csv) | Field dictionary and legend |

Encoding: **UTF-8**, comma-separated, dates in **ISO 8601** (`YYYY-MM-DD`), LF line endings. Column names stay in French, as in the CSV.

## Columns in `inventaire.csv`

| Column | Meaning |
|---|---|
| `id` | Stable ASCII slug |
| `nom` | System name |
| `editeur` | Publisher or maintainer |
| `categorie` | Inventory category |
| `cible` | Deployment context: Individuel, Équipe, Entreprise, Workflows métier, Infrastructure, Recherche |
| `metiers` | Jobs the product officially targets (`Dev`, `Science`, `Mkt`…). `Généraliste` if it is not job-specific |
| `acces` | Open source, hybrid, proprietary… |
| `licence` | Documented license or terms |
| `maturite` | Active, experimental, archived… |
| `surfaces` | CLI, IDE, web, cloud… |
| `local` / `cloud` | Where it runs |
| `politique_modeles` | Supported models |
| `terminal` `ide` `web` `computer_use` | Interaction surfaces |
| `mcp` `acp` `skills` `sous_agents` | Protocols and composition |
| `memoire` `sandbox` `orchestration` | Memory, isolation, coordination |
| `usage_principal` | Main observed use |
| `source_principale` | Reference URL |
| `type_source` | Primary / repo or secondary / index |
| `notes` | Occasional remark |
| `confiance` | Reliability of the row, not of the product (`Élevée` / `Moyenne` / `Faible`) |
| `verifie_le` | Verification date |
| `definition_categorie` `est_harness` `remarque_categorie` | Joined from `taxonomie.csv` |

## Breakdown

**Categories**

| Category | n |
|---|---|
| Coding harness | 42 |
| Framework / SDK | 26 |
| Orchestrator | 24 |
| Research coding agent | 23 |
| Research science agent | 6 |
| Meta-harness / workspace | 12 |
| Agentic IDE | 10 |
| General-purpose agent | 12 |
| Cloud coding agent | 8 |
| App-building agent | 7 |
| Coding agent | 4 |
| Agent runtime | 3 |
| Autonomous loop | 2 |
| Agent platform | 1 |
| Agent bridge | 1 |
| Review / coding agent | 1 |
| Review agent | 1 |

**Access**: 82 open source · 53 proprietary · 23 open source / research · 17 open source / hybrid · 8 other.

**Confidence**: 97 high · 83 medium · 3 low.

**Cible**: 77 individual · 34 team · 29 infrastructure · 28 research · 14 enterprise · 1 business workflows.

**Métiers**: 136 Dev · 34 generalist · 6 Science · 7 with extra documented jobs (Data, Ops, Sec, OpenWorker’s set, or Paperclip’s business set).

## Scope

In scope: coding harnesses, general-purpose agents that can write code, science agents, agent platforms, orchestrators, and adjacent frameworks.

Out of scope: models alone, plain autocomplete with no agent loop, unidentified small forks, and short-lived wrappers.

Method: official docs and repositories first; community lists for the long tail. Licenses and features should be rechecked before any legal use.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). One pull request per tool, official source required, no guessed cells.

## Usage

```bash
# preview
head -n 2 inventaire.csv

# Python
python3 -c "import csv; rows=list(csv.DictReader(open('inventaire.csv', encoding='utf-8'))); print(len(rows), rows[0]['nom'])"
```

## License

This dataset is licensed under [CC BY 4.0](LICENSE). You can reuse and adapt it, including commercially, as long as you give credit. See [CITATION.cff](CITATION.cff) if you cite it.

Project licenses listed in the CSV belong to those projects, not to this inventory.
