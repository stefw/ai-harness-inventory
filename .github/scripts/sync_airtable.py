#!/usr/bin/env python3
"""Upsert inventaire.csv vers Airtable via l'API REST (plan gratuit inclus)."""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BATCH = 10
PAUSE = 0.25
MERGE_FIELD = "id"


def env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"Variable manquante : {name}", file=sys.stderr)
        sys.exit(1)
    return value


def request(method: str, url: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {env('AIRTABLE_PAT')}")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8", errors="replace"), file=sys.stderr)
        raise


def paced(method: str, url: str, body: dict | None = None) -> dict:
    time.sleep(PAUSE)
    return request(method, url, body)


def chunks(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        print("inventaire.csv est vide", file=sys.stderr)
        sys.exit(1)
    if MERGE_FIELD not in rows[0]:
        print(f"Colonne {MERGE_FIELD} absente du CSV", file=sys.stderr)
        sys.exit(1)
    return rows


def record_fields(row: dict) -> dict:
    return {key: value for key, value in row.items() if value != ""}


def find_table(base: str, table_ref: str) -> dict:
    payload = paced("GET", f"https://api.airtable.com/v0/meta/bases/{base}/tables")
    tables = payload.get("tables", [])
    for table in tables:
        if table.get("id") == table_ref or table.get("name") == table_ref:
            return table
    names = ", ".join(f"{t.get('name')} ({t.get('id')})" for t in tables) or "(aucune)"
    print(f"Table introuvable : {table_ref}. Tables : {names}", file=sys.stderr)
    sys.exit(1)


def ensure_fields(base: str, table: dict, columns: list[str]) -> None:
    existing = {field.get("name") for field in table.get("fields", [])}
    missing = [name for name in columns if name not in existing]
    if not missing:
        return
    table_id = table["id"]
    print(f"Champs Airtable manquants : {', '.join(missing)}")
    for name in missing:
        try:
            paced(
                "POST",
                f"https://api.airtable.com/v0/meta/bases/{base}/tables/{table_id}/fields",
                {"name": name, "type": "singleLineText"},
            )
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 403}:
                print(
                    "Le token Airtable ne peut pas créer de champs "
                    "(scope schema.bases:write requis), "
                    f"ou crée-les à la main : {', '.join(missing)}",
                    file=sys.stderr,
                )
            raise
        print(f"Champ créé : {name}")


def list_existing(api: str) -> list[dict]:
    records: list[dict] = []
    offset = None
    while True:
        query = {"pageSize": "100", "fields[]": MERGE_FIELD}
        if offset:
            query["offset"] = offset
        url = f"{api}?{urllib.parse.urlencode(query)}"
        payload = paced("GET", url)
        records.extend(payload.get("records", []))
        offset = payload.get("offset")
        if not offset:
            return records


def main() -> None:
    csv_path = Path(os.environ.get("INVENTAIRE_CSV", "inventaire.csv"))
    base = env("AIRTABLE_BASE_ID")
    table = env("AIRTABLE_TABLE")
    api = f"https://api.airtable.com/v0/{base}/{urllib.parse.quote(table, safe='')}"

    rows = load_csv(csv_path)
    ensure_fields(base, find_table(base, table), list(rows[0].keys()))
    created = updated = deleted = 0

    for batch in chunks(rows, BATCH):
        payload = paced(
            "PATCH",
            api,
            {
                "performUpsert": {"fieldsToMergeOn": [MERGE_FIELD]},
                "typecast": True,
                "records": [{"fields": record_fields(row)} for row in batch],
            },
        )
        created += len(payload.get("createdRecords", []))
        updated += len(payload.get("updatedRecords", []))

    csv_ids = {row[MERGE_FIELD] for row in rows}
    stale = [
        rec["id"]
        for rec in list_existing(api)
        if rec.get("fields", {}).get(MERGE_FIELD) not in csv_ids
    ]
    for batch in chunks(stale, BATCH):
        query = "&".join(f"records[]={urllib.parse.quote(rec_id)}" for rec_id in batch)
        paced("DELETE", f"{api}?{query}")
        deleted += len(batch)

    print(
        f"Sync OK : {len(rows)} lignes CSV, "
        f"{created} créées, {updated} mises à jour, {deleted} supprimées"
    )


if __name__ == "__main__":
    main()
