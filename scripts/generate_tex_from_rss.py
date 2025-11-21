#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import feedparser
from datetime import datetime

# Fichier CSV généré par generate_rss.py
CSV_FILE = "rss_feeds.csv"
OUTPUT_TEX = "press_review.tex"

def read_rss_csv(file_path):
    feeds = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            feeds.append({"company": row["Company"], "url": row["RSS Feed URL"]})
    return feeds

def fetch_articles(feed_url, limit=5):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:limit]:
        articles.append({"title": entry.title, "link": entry.link})
    return articles

def generate_latex(feeds):
    today = datetime.now().strftime("%d %B %Y")
    tex_content = [
        "\\documentclass[11pt,a4paper]{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage{hyperref}",
        "\\usepackage{geometry}",
        "\\geometry{margin=1in}",
        "\\title{BeLux Weekly Press Review}",
        f"\\date{{{today}}}",
        "\\begin{document}",
        "\\maketitle",
        "\\section*{Summary}",
        "This weekly press review focuses on Belgium and Luxembourg companies.",
        "\\vspace{1cm}"
    ]

    for feed in feeds:
        tex_content.append(f"\\section*{{{feed['company']}}}")
        articles = fetch_articles(feed["url"])
        if not articles:
            tex_content.append("\\textit{No recent articles found.}")
        else:
            for art in articles:
                tex_content.append(f"\\textbf{{{art['title']}}}\\\\")
                tex_content.append(f"\\href{{{art['link']}}}{{Read more}}\\\\[0.5em]")

    tex_content.append("\\end{document}")
    return "\n".join(tex_content)

def main():
    feeds = read_rss_csv(CSV_FILE)
    latex_code = generate_latex(feeds)
    with open(OUTPUT_TEX, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"[OK] LaTeX file generated: {OUTPUT_TEX}")

if __name__ == "__main__":
    main()
