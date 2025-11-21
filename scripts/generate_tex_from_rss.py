#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import feedparser
from datetime import datetime

CSV_FILE = "rss_feeds.csv"
OUTPUT_TEX = "press_review.tex"

# Échappement LaTeX : traiter d'abord le backslash
LATEX_ESCAPE_ORDERED = [
    ("\\", r"\\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
 dicts."""    ("$", r"\$"),
    feeds = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            feeds.append({"company": row["Company"], "url": row["RSS Feed URL"]})
    return feeds

def fetch_articles(feed_url: str, limit: int = 5):
    """Récupère jusqu'à 'limit' articles depuis un flux RSS."""
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:limit]:
        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "")
        articles.append({"title": title, "link": link})
    return articles

def generate_latex(feeds):
    """Génère le contenu LaTeX pour la revue de presse."""
    # Date en anglais pour cohérence avec LaTeX standard (ou adapte selon besoin)
    today = datetime.now().strftime("%d %B %Y")

    # Préambule LaTeX minimal compatible tectonic
    tex_lines = [
        r"\documentclass[11pt,a4paper]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{hyperref}",
        r"\usepackage{geometry}",
        r"\geometry{margin=1in}",
        r"\title{BeLux Weekly Press Review}",
        rf"\date{{{escape_latex(today)}}}",
        r"\begin{document}",
        r"\maketitle",
        r"\section*{Summary}",
        r"This weekly press review focuses on Belgium and Luxembourg companies.",
        r"\vspace{1cm}",
    ]

    for feed in feeds:
        company_name = escape_latex(feed["company"])
        tex_lines.append(rf"\section*{{{company_name}}}")

        articles = fetch_articles(feed["url"])
        if not articles:
            tex_lines.append(r"\textit{No recent articles found.}")
        else:
            for art in articles:
                title = escape_latex(art["title"])
                # Pour les URL, éviter d'échapper trop agressivement (hyperref gère souvent bien)
                # On échappe quand même les caractères problématiques
                link = escape_latex(art["link"])
                tex_lines.append(rf"\textbf{{{title}}}\\")
                tex_lines.append(rf"\href{{{link}}}{{Read more}}\\[0.5em]")

    tex_lines.append(r"\end{document}")
    return "\n".join(tex_lines)

def main():
    feeds = read_rss_csv(CSV_FILE)
    latex_code = generate_latex(feeds)
    with open(OUTPUT_TEX, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"[OK] LaTeX file generated: {OUTPUT_TEX}")

if __name__ == "__main__":
    main()
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]

def escape_latex(text: str) -> str:
    """Échappe les caractères spéciaux LaTeX dans une chaîne."""
    if not isinstance(text, str):
        text = str(text)
    for char, repl in LATEX_ESCAPE_ORDERED:
        text = text.replace(char, repl)
    return text

def read_rss_csv(file_path: str):
