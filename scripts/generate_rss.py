#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os

KEYWORDS = (
    "(innovation+OR+HR+OR+production+OR+business+OR+strategy+OR+leadership+"
    "OR+sustainability+OR+ESG+OR+digital+transformation+OR+AI+OR+mergers+OR+"
    "acquisitions+OR+finance+OR+operations+OR+supply+chain+OR+management)"
)

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

def build_geo_filter_and_region(location: str):
    if location == "Belgium":
        return '("Belgium"+OR+"Brussels")', "&hl=en&gl=BE&ceid=BE:en"
    else:
        return '("Luxembourg"+OR+"Betzdorf")', "&hl=en&gl=LU&ceid=LU:en"

def build_company_query(name: str, location: str) -> str:
    q_name = name.replace(" ", "+")
    geo_filter, region = build_geo_filter_and_region(location)
    return f'https://news.google.com/rss/search?q="%s"+%s+%s%s' % (q_name, KEYWORDS, geo_filter, region)

def main():
    out_file = os.environ.get("RSS_CSV_PATH", "rss_feeds.csv")
    rows = []
    for c in COMPANIES:
        url = build_company_query(c["name"], c["location"])
        rows.append([c["name"], url])

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Company", "RSS Feed URL"])
        w.writerows(rows)

    print(f"[OK] CSV généré: {out_file} ({len(rows)} lignes)")

if __name__ == "__main__":
    main()
