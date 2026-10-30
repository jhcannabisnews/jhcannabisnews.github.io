"""Write search + share-preview tags (description, Open Graph, X card) into every page,
and regenerate sitemap.xml. Run after adding a page: py -3 tools/sync_meta.py
"""
import glob, html, os, re
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://jhcannabisnews.com/"
DESC = {
    "index.html": "Cannabis law news every day with James & Hope: federal rescheduling, the hemp ban, state laws and every ballot vote, explained in plain English.",
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
    "texas-delta-8-felony-hemp-ban.html": "Texas made delta-8, THCA flower and other hemp THC a felony to possess. What's still legal, the court fight, and the federal hemp ban dates: Nov 12 and Dec 11.",
    "rescheduling-stalled-again.html": "A DEA judge gave rescheduling opponents more time. Who is fighting it, why both Massachusetts senators oppose Question 8, and Pennsylvania's Ryan's Law vote.",
    "marijuana-rescheduling-paused.html": "A DEA judge paused marijuana rescheduling. Medical moved to Schedule III in April; here's what happens to the rest, plus Massachusetts Question 8 and the hemp ban.",
    "cannabis-on-the-ballot-2026.html": "Every cannabis vote on Nov 3, 2026: Houston Proposition A, Idaho HJR 4 and Massachusetts Question 8, explained, plus Ohio's new limits.",
    "election.html": "Cannabis on the ballot Nov 3, 2026: Massachusetts Question 8, Idaho HJR 4 and Houston Proposition A. What yes and no mean, plus live election-night results.",
    "checker.html": "Is weed legal in my state? Check recreational marijuana, medical marijuana and delta-8 / hemp THC laws in all 50 states, plus the federal hemp ban dates. Updated October 2026.",
    "federal-hemp-ban-explained.html": "The federal hemp ban explained: what happens to delta-8, THCA flower, THC gummies and drinks on Nov 12 and Dec 11, 2026, how the ban got delayed, and what it means for you.",
    "bills.html": "Texas cannabis bill tracker for the 90th Legislature (2027): every marijuana, hemp and THC bill filed, and how far each one has gotten. Updated twice a day.",
    "ask.html": "Send James & Hope your cannabis-law question about your state. We answer the best ones on the show.",
    "about.html": "About J&H Cannabis News: who James & Hope are, how the show is made, and our sources.",
}
ARTICLES = {"federal-hemp-ban-explained.html", "texas-delta-8-felony-hemp-ban.html", "marijuana-rescheduling-paused.html", "cannabis-on-the-ballot-2026.html", "rescheduling-stalled-again.html"}
START, END = "<!-- meta -->", "<!-- /meta -->"
pages = []
for path in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    page = os.path.basename(path)
    t = open(path, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    if not m:          # e.g. the Search Console verification file
        continue
    if page == "merch-preview-jh7q.html":   # private preview: no tags, never in the sitemap
        continue
    if page == "merch.html":                # tools/build_merch.py writes its own head
        pages.append(BASE + page)
        continue
    title = html.unescape(m.group(1).strip())
    desc = DESC.get(page) or DESC["index.html"]
    url = BASE + ("" if page == "index.html" else page)
    e = lambda s: html.escape(s, quote=True)
    block = "\n".join([START,
        f'<meta name="description" content="{e(desc)}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:site_name" content="J&amp;H Cannabis News">',
        f'<meta property="og:type" content="{"article" if page in ARTICLES else "website"}">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}og-image.jpg">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{BASE}og-image.jpg">',
        # Cloudflare Web Analytics (cookie-free visitor counts; the token is public by design)
        '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
        """data-cf-beacon='{"token": "af0be1d6d28d4b12a34e29dee0df9b78"}'></script>""",
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
