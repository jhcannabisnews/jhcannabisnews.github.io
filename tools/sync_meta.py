"""Write search + share-preview tags (description, Open Graph, X card) into every page,
and regenerate sitemap.xml. Run after adding a page: py -3 tools/sync_meta.py
"""
import glob, html, os, re
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://jhcannabisnews.github.io/"
DESC = {
    "index.html": "Cannabis law news every weekday with James & Hope: federal rescheduling, the hemp ban, state laws and every ballot vote, explained in plain English.",
    "episodes.html": "Every J&H Cannabis News episode: the day's biggest cannabis-law stories with real local news clips, explained by James & Hope.",
    "shorts.html": "The biggest cannabis-law story of each episode in under a minute, from J&H Cannabis News.",
    "states.html": "Interactive map of cannabis and hemp laws in all 50 states, with the latest news for each state.",
    "headlines.html": "Today's cannabis-law headlines from across the country, refreshed twice a day.",
    "watchlist.html": "Every cannabis-law date that matters: court hearings, ballot votes and federal hemp deadlines, with countdowns.",
    "explainers.html": "Plain-English explainers on cannabis law: delta-8, THCA, hemp vs. marijuana, and what Schedule I really means.",
    "explain-delta-8.html": "How delta-8 THC became legal through the 2018 Farm Bill, and why state bans and the federal rewrite are ending it.",
    "explain-hemp-vs-marijuana.html": "The legal line between hemp and marijuana: the 0.3% delta-9 THC rule, total THC, and what's changing.",
    "explain-schedule-1.html": "What Schedule I actually means under federal law, and what moving marijuana to Schedule III does and doesn't change.",
    "explain-thca.html": "THCA vs. delta-9: why 'hemp flower' gets you high, and how total-THC testing rules are closing the loophole.",
    "ask.html": "Send James & Hope your cannabis-law question about your state. We answer the best ones on the show.",
    "about.html": "About J&H Cannabis News: who James & Hope are, how the show is made, and our sources.",
}
START, END = "<!-- meta -->", "<!-- /meta -->"
pages = []
for path in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    page = os.path.basename(path)
    t = open(path, encoding="utf-8").read()
    title = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1).strip())
    desc = DESC.get(page) or DESC["index.html"]
    url = BASE + ("" if page == "index.html" else page)
    e = lambda s: html.escape(s, quote=True)
    block = "\n".join([START,
        f'<meta name="description" content="{e(desc)}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:site_name" content="J&amp;H Cannabis News">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}og-image.jpg">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{BASE}og-image.jpg">',
        END])
    if START in t:
        t2 = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, t, flags=re.S)
    else:
        t2 = re.sub(r"(</title>\n?)", lambda m: m.group(1) + block + "\n", t, count=1)
    if t2 != t:
        open(path, "w", encoding="utf-8", newline="\n").write(t2); print("updated:", page)
    pages.append(url)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"  <url><loc>{u}</loc></url>" for u in pages] + ["</urlset>", ""]
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm))
open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8", newline="\n").write(
    f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print(len(pages), "pages in sitemap.xml")
