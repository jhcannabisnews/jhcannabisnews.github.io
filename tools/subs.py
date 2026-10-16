"""Keep the home page's 500-subscriber goal bar current: read the channel's public subscriber count
and rewrite the bar width and "N of 500 subscribers" text in index.html. Runs hourly from
.github/workflows/subs.yml; by hand: python3 tools/subs.py
If YouTube can't be read (bot wall, layout change), it leaves the page alone and exits 1 so the run shows as failed."""
import os, re, sys, urllib.request

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://www.youtube.com/@jhcannabisnews/about?hl=en&gl=US"
GOAL = 500


def count():
    req = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "CONSENT=YES+1; SOCS=CAI",
    })
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = re.search(r'"(\d[\d.,]*)\s*([KM]?) subscribers"', page) or re.search(r'>(\d[\d.,]*)\s*([KM]?) subscribers<', page)
    if not m:
        return None
    n = float(m.group(1).replace(",", ""))
    return int(round(n * {"": 1, "K": 1_000, "M": 1_000_000}[m.group(2)]))


def main():
    try:
        n = count()
    except Exception as e:
        print("could not read YouTube:", e); return 1
    if not n:
        print("subscriber count not found; page left alone"); return 1
    pct = max(1, min(100, round(n * 100 / GOAL)))
    p = os.path.join(SITE, "index.html")
    t = open(p, encoding="utf-8").read()
    t2 = re.sub(r'(<div id="subs-fill" style="width:)\d+%', rf"\g<1>{pct}%", t)
    text = f"{n:,} of {GOAL} subscribers" if n < GOAL else f"{n:,} subscribers. We made it! 🎉"
    t2 = re.sub(r'(<p id="subs-text"[^>]*>)[^<]*', rf"\g<1>{text}", t2)
    if t2 != t:
        open(p, "w", encoding="utf-8", newline="\n").write(t2)
    print("subscribers:", n, f"({pct}%)", "updated" if t2 != t else "unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
