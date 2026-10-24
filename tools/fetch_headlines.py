"""Build data/headlines.json from Google News RSS (cannabis-law queries).

Runs twice a day in GitHub Actions (.github/workflows/headlines.yml); standard library only.
"""
import datetime as dt
import email.utils
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

QUERIES = [
    "cannabis law", "marijuana legalization", "hemp THC ban", "delta-8 ban",
    "marijuana ballot measure", "cannabis bill legislature", "hemp federal ban",
    "marijuana rescheduling DEA",
]
RELEVANT = re.compile(r"cannabis|marijuana|hemp|\bthc|\bcbd|delta-?8|delta-?9|weed|dispensar|thca", re.I)
# "House"/"Senate" alone are usually STATE chambers, so they do not count as federal.
FEDERAL = re.compile(r"\bcongress|\bfederal|\bdea\b|\bfda\b|u\.s\. senate|white house|reschedul|farm bill|trump", re.I)
# The show is U.S. law news: drop foreign stories and drug-bust crime items.
FOREIGN = re.compile(
    r"nigeria|ndlea|taiwan|canad|thai|new zealand|\bnz\b|australia|\buk\b|brit|england|scotland|"
    r"ireland|german|south africa|india|philippin|mexic|colombia|uruguay|europe|\beu\b|japan|korea|"
    r"malaysia|singapore|indonesia|ghana|kenya|jamaica|israel|morocco|pakistan|lebanon|ukrain|spain|"
    r"france|ital|netherland|dutch|swiss|czech|poland|brazil|argentin|chile|peru\b|china|chinese|"
    r"africa|\bctv\b|intellinews",
    re.I)
CRIME = re.compile(r"\barrest|\bseiz|\bnabbed|\bbust\b|smuggl|traffick|\bkilos?\b|tonnes?|\bkg\b", re.I)
MARKETS = re.compile(r"\bstocks?\b|\bshares\b|better buy|weedcoin|crypto|motley fool|stocktwits", re.I)
ALIASES = {"Mass.": "Massachusetts", "D.C.": "Washington, D.C.", "Calif.": "California"}
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
          "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
          "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
          "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
          "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
          "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
          "Washington", "West Virginia", "Wisconsin", "Wyoming"]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "headlines.json")
MAX_ITEMS = 60


def fetch(query):
    q = urllib.parse.quote(f"{query} when:3d")
    url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "JHCannabisNews/1.0 (+https://jhcannabisnews.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return ET.fromstring(r.read())


def tags_for(title):
    tags = [s for s in STATES if re.search(rf"\b{s}\b", title)]
    # "West Virginia" also matches "Virginia"; "Arkansas" also matches "Kansas"
    if "West Virginia" in tags and "Virginia" in tags and not re.search(r"(?<!West )Virginia", title):
        tags.remove("Virginia")
    if "Kansas" in tags and not re.search(r"(?<!Ar)kansas", title, re.I):
        tags.remove("Kansas")
    for alias, state in ALIASES.items():
        if alias in title and state not in tags:
            tags.append(state)
    if FEDERAL.search(title):
        tags.insert(0, "Federal")
    return tags


def main():
    seen, items = set(), []
    for query in QUERIES:
        try:
            root = fetch(query)
        except Exception as e:  # one failed query must not kill the run
            print(f"query failed: {query!r}: {e}")
            continue
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            src_el = it.find("source")
            source = (src_el.text or "").strip() if src_el is not None else ""
            if source and title.endswith(" - " + source):
                title = title[: -len(source) - 3]
            key = re.sub(r"\W+", "", title.lower())[:80]
            if (not title or key in seen or not RELEVANT.search(title)
                    or FOREIGN.search(title) or FOREIGN.search(source) or CRIME.search(title)
                    or MARKETS.search(title) or MARKETS.search(source)):
                continue
            seen.add(key)
            try:
                published = email.utils.parsedate_to_datetime(it.findtext("pubDate")).astimezone(dt.timezone.utc)
            except Exception:
                continue
            items.append({"title": title, "source": source, "url": it.findtext("link"),
                          "published": published.isoformat(), "tags": tags_for(title)})
    items.sort(key=lambda x: x["published"], reverse=True)
    data = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "items": items[:MAX_ITEMS]}
    if not data["items"]:
        raise SystemExit("no headlines fetched; keeping the previous file")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(data['items'])} headlines")


if __name__ == "__main__":
    main()
