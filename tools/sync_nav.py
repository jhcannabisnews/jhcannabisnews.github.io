"""Write the one canonical nav bar into every page (marks the current page active).

Run after adding or renaming a page: py -3 tools/sync_nav.py
"""
import glob
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = [("index.html", "Home"), ("episodes.html", "Episodes"), ("shorts.html", "Shorts"),
        ("states.html", "States"), ("headlines.html", "Headlines")]
MORE = [("explainers.html", "Explainers"), ("watchlist.html", "Watch List"),
        ("ask.html", "Ask James &amp; Hope"), ("about.html", "About")]
NAV_RE = re.compile(r"<nav>.*?</nav>", re.S)


def nav_for(page):
    current = "explainers.html" if page.startswith("explain-") else page
    def link(href, label):
        cls = ' class="active"' if href == current else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    more_active = ' class="active"' if current in {h for h, _ in MORE} else ""
    lines = ['<nav>', '  <img src="logo.png" alt=""><span class="brand">J&amp;H CANNABIS NEWS</span>']
    lines += [f"  {link(h, l)}" for h, l in MAIN]
    lines.append(f"  <details><summary{more_active}>More ▾</summary><div class=\"menu\">")
    lines += [f"    {link(h, l)}" for h, l in MORE]
    lines += ["  </div></details>", "</nav>"]
    return "\n".join(lines)


for path in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    page = os.path.basename(path)
    html = open(path, encoding="utf-8").read()
    if not NAV_RE.search(html):
        print(f"skip (no nav): {page}")
        continue
    new = NAV_RE.sub(lambda _: nav_for(page), html, count=1)
    if new != html:
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        print(f"updated: {page}")
