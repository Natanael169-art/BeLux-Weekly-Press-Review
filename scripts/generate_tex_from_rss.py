#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import feedparser
from datetime import datetime

CSV_FILE = "rss_feeds.csv"
OUTPUT_TEX = "press_review.tex"

# LaTeX escaping
LATEX_ESCAPE_ORDERED = [
    ("\\", r"\\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]

LOCATION_FILTER = ["Belgium", "Brussels", "Luxembourg", "Betzdorf"]

def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    for char, repl in LATEX_ESCAPE_ORDERED:
        repl)
    return text

def escape_url_for_latex(url: str) -> str:
    if not isinstance(url, str):
        url = str(url)
    return url.replace("%", r"\%").replace("#", r"\#")

def read_rss_csv(file_path: str):
    feeds = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            feeds.append({"company": row["Company"], "url": row["RSS Feed URL"]})
    return feeds

def fetch_articles(feed_url: str, limit: int = 5):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in getattr(feed, "entries", []):
        title = getattr(entry, "title", "")
        summary = getattr(entry, "summary", "")
        # Filtrage par mots-clés géographiques
        if any(loc in (title + summary) for loc in LOCATION_FILTER):
            articles.append({"title": title, "link": getattr(entry, "link", "")})
        if len(articles) >= limit:
            break
    return articles

def generate_latex(feeds):
    today = datetime.now().strftime("%d %B %Y")
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
            tex_lines.append(r"\textit{No relevant articles found for Belgium/Luxembourg.}")
        else:
            for art in articles:
                title = escape_latex(art["title"])
                link = escape_url_for_latex(art["link"])
                tex_lines.append(rf"\textbf{{{title}}}\\")
                tex_lines.append(rf"\href{{{link}}}{{Read more}}\\[0.8em]")

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
