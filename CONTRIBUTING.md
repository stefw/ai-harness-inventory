# Contributing

This repository is a curated inventory. GitHub is the source of truth. Please do not invent facts to fill a cell.

## Add or fix an entry

Open a pull request that changes `inventaire.csv` (and `sources.csv` if you add a URL).

Rules:

1. One tool per pull request.
2. Point `source_principale` at the official repository or documentation, not an awesome-list or a GitHub search.
3. Keep column names as they are. Do not rename fields.
4. Keep `id` stable. Only change it if the project itself was renamed.
5. Use `Inconnu / non documenté` when a feature is not confirmed. That is not the same as `Non`.
6. Set `confiance` to `Élevée` only if the official source was checked. Use `Moyenne` for a partial official source. Use `Faible` only as a last resort.
7. Do not guess `licence`, `mcp`, `acp`, `cible`, or `metiers`. Leave them unknown rather than approximating.
8. `cible` is one of: Individuel, Équipe, Entreprise, Workflows métier, Infrastructure, Recherche.
9. `metiers` uses only: Dev, Data, Ops, Sec, Com, Mkt, RH, Support, Sales, Finance, Science, Généraliste. Do not add Com / Mkt / RH / Science unless the official docs say so. A coding harness is `Dev`, not an implied HR or science tool.

If the category is new, add it to `taxonomie.csv` with a short definition.

## Out of scope

Do not add:

- models alone
- autocomplete without an agent loop
- unidentified forks
- short-lived wrappers

## After merge

A change to `inventaire.csv` on `main` updates the public Airtable view. You do not need to edit Airtable by hand.
