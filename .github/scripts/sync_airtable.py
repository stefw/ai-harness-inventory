#!/usr/bin/env python3
"""Upsert inventaire.csv vers Airtable via l'API REST (plan gratuit inclus)."""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BATCH = 10
PAUSE = 0.25
MERGE_FIELD = "id"
UNKNOWN_FIELD = re.compile(r'Unknown field name: "([^"]+)"')


class AirtableError(RuntimeError):
    def __init__(self, status: int, payload: dict):
        self.status = status
        self.payload = payload
        super().__init__(json.dumps(payload, ensure_ascii=False))


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
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"error": {"message": raw}}
        print(raw, file=sys.stderr)
        raise AirtableError(exc.code, payload) from exc


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


def unknown_field(error: AirtableError) -> str | None:
    err = error.payload.get("error") or {}
    if err.get("type") != "UNKNOWN_FIELD_NAME":
        return None
    match = UNKNOWN_FIELD.search(err.get("message") or "")
    return match.group(1) if match else None


def record_fields(row: dict, skip: set[str]) -> dict:
    return {
        key: value
        for key, value in row.items()
        if value != "" and key not in skip
    }


def upsert(api: str, rows: list[dict]) -> tuple[int, int, set[str]]:
    skip: set[str] = set()
    created = updated = 0
    index = 0
    batches = list(chunks(rows, BATCH))
    while index < len(batches):
        batch = batches[index]
        try:
            payload = paced(
                "PATCH",
                api,
                {
                    "performUpsert": {"fieldsToMergeOn": [MERGE_FIELD]},
                    "typecast": True,
                    "records": [
                        {"fields": record_fields(row, skip)} for row in batch
                    ],
                },
            )
        except AirtableError as error:
            field = unknown_field(error)
            if not field:
                raise
            if field == MERGE_FIELD:
                print(f"Le champ de fusion {MERGE_FIELD} est absent d'Airtable", file=sys.stderr)
                sys.exit(1)
            print(f"Champ Airtable absent, ignoré : {field}")
            skip.add(field)
            continue
        created += len(payload.get("createdRecords", []))
        updated += len(payload.get("updatedRecords", []))
        index += 1
    return created, updated, skip


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
    created, updated, skipped = upsert(api, rows)
    deleted = 0

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
    if skipped:
        print(
            "Crée ces champs texte dans Airtable (noms exacts), puis relance la sync : "
            + ", ".join(sorted(skipped))
        )


if __name__ == "__main__":
    main()
