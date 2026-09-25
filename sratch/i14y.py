"""Build the party codelist from parteienatlas CSVs and upload it to I14Y."""
 
import json
from pathlib import Path
import pandas as pd
import requests
from config import TOKEN, entry_uid
 
API_BASE = "https://api-a.i14y.admin.ch/api/partner/v1"
LANG_MAP = {"de-CH": "de", "fr-CH": "fr", "it-CH": "it", "en-US": "en"}
 
 
def build_party_entries(data_dir="."):
    path = Path(data_dir)
    party = pd.read_csv(path / "party.csv", encoding="utf-8-sig")
    party_name = pd.read_csv(path / "party_name.csv", encoding="utf-8-sig", parse_dates=["from_date_datetime"])
 
    latest_names = party_name.sort_values("from_date_datetime").groupby("party_id").last()
   
    entries = []
    for party_id in party["party_id"]:
        if party_id not in latest_names.index:
            continue
        row = latest_names.loc[party_id]
 
        name, abbr = {}, {}
        for i in range(1, 5):
            lang = LANG_MAP.get(row.get(f"translations_languages_code{i}"))
            if lang:
                if pd.notna(val := row.get(f"translations_name{i}")):
                    name[lang] = val
                if pd.notna(val := row.get(f"translations_abbreviation{i}")):
                    abbr[lang] = val
 
        if name:
            entry = {"code": str(party_id), "name": name}
            if abbr:
                entry["annotations"] = [{"type": "Abbreviation", "text": abbr}]
            entries.append(entry)
 
    return entries
 
 
def main():
    headers = {"Authorization": TOKEN}
 
    # 1. Bisherige Codelist-Einträge löschen (Replace)
    requests.delete(
        f"{API_BASE}/concepts/{entry_uid}/codelist-entries",
        headers=headers
    ).raise_for_status()
 
    # 2. Neue Einträge bauen und importieren
    entries = build_party_entries()
    payload = {"data": [{**e, "conceptId": entry_uid} for e in entries]}
 
    resp = requests.post(
        f"{API_BASE}/concepts/{entry_uid}/codelist-entries/imports/Json",
        headers=headers,
        files={"file": ("party-codelist.json", json.dumps(payload), "application/json")},
    )
    if not resp.ok:
        print(resp.text)
    resp.raise_for_status()
 
    print(f"Import von {len(entries)} Einträgen erfolgreich beendet (Status {resp.status_code}).")
 
 
if __name__ == "__main__":
    main()