#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os

# --- Paramètres globaux ---
KEYWORDS = (
    "(innovation+OR+HR+OR+production+OR+business+OR+strategy+OR+leadership+"
    "OR+sustainability+OR+ESG+OR+digital+transformation+OR+AI+OR+mergers+OR+"
    "acquisitions+OR+finance+OR+operations+OR+supply+chain+OR+management)"
)

# Entreprises et pays (d’après les adresses que tu as fournies)
COMPANIES = [
    {"name": "Barco", "location": "Belgium"},
    {"name": "Husky", "location": "Belgium"},
    {"name": "SES", "location": "Luxembourg"},
    {"name": "Agfa Gevaert", "location": "Belgium"},
    {"name": "Danone", "location": "Belgium"},
    {"name": "Total", "location": "Belgium"},
    {"name": "IMEC", "location": "Belgium"},
    {"name": "Arval", "location": "Belgium"},
    {"name": "Vinci", "location": "Belgium"},
    {"name": "Coca Cola", "location": "Belgium"},
    {"name": "Unilin", "location": "Belgium"},
    {"name": "Etex", "location": "Belgium"},
    {"name": "Sodexo", "location": "Belgium"},
    {"name": "Ontex", "location": "Belgium"},
    {"name": "Toyota", "location": "Belgium"},
]

# Filtre géographique strict (ajouté à la requête Google News)
# - Belgique : ("Belgium" OR "Brussels")
# - Luxembourg : ("Luxembourg" OR "Betzdorf")
def build_geo_filter_and_region(location: str):
    if location == "Belgium":
        geo_filter = '("Belgium"+OR+"Brussels")'
        region = "&hl=en&gl=BE&ceid=BE:en"
    else:  # Luxembourg
        geo_filter = '("Luxembourg"+OR+"Betzdorf")'
        region = "&hl=en&gl=LU&ceid=LU:en"
    return geo_filter, region

def build_company_query(name: str, location: str) -> str:
    # Nom encodé pour l’URL (espaces -> +)
    q_name = name.replace(" ", "+")
    geo_filter, region = build_geo_filter_and_region(location)
    return (
        f'https://news.google.com/rss/search?q="%s"+%s+%s%s'
        % (q_name, KEYWORDS, geo_filter, region)
    )

def main():
    out_file = os.environ.get("RSS_CSV_PATH", "rss_feeds.csv")
    rows = []

    for c in COMPANIES:
        url = build_company_query(c["name"], c["location"])
        rows.append([c["name"], url])

    # Écriture du CSV
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Company", "RSS Feed URL"])
        w.writerows(rows)

    print(f"[OK] CSV généré: {out_file} ({len(rows)} lignes)")

if __name__ == "__main__":
    main()
